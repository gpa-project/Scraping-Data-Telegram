import asyncio
import os
import sys
from datetime import datetime

try:
    from telethon import TelegramClient
    from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
except ImportError as e:
    print("❌ Error import Telethon:", e)
    print("📦 Coba install: pip install telethon --upgrade")
    sys.exit(1)

class TelegramBackupPrivate:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient(f'session_{phone_number}', api_id, api_hash)
        
    async def connect(self):
        """Connect to Telegram"""
        await self.client.start(phone=self.phone_number)
        print("✅ Berhasil connect ke Telegram!")
        
    async def list_dialogs(self):
        """List semua chat/channel yang bisa diakses"""
        print("\n📋 Daftar Chat/Channel:")
        print("-" * 50)
        
        async for dialog in self.client.iter_dialogs():
            if dialog.is_channel or dialog.is_group:
                print(f"📁 Nama: {dialog.name}")
                print(f"   ID: {dialog.id}")
                print(f"   Tipe: {'Channel' if dialog.is_channel else 'Group'}")
                if hasattr(dialog.entity, 'username') and dialog.entity.username:
                    print(f"   Username: @{dialog.entity.username}")
                else:
                    print(f"   Username: [PRIVATE]")
                print(f"   Pesan: {dialog.message.id if dialog.message else 'N/A'}")
                print("-" * 30)
        
        print("\n💡 Copy ID channel yang ingin dibackup!")
        
    async def backup_by_id(self, channel_id):
        """Backup channel menggunakan ID"""
        
        download_path = "./download"
        os.makedirs(download_path, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(download_path, f"backup_private_{timestamp}")
        os.makedirs(backup_folder, exist_ok=True)
        
        print(f"📁 Menyimpan file di: {os.path.abspath(backup_folder)}")
        
        try:
            # Convert ID ke integer jika perlu
            if isinstance(channel_id, str):
                channel_id = int(channel_id)
                
            # Get channel entity by ID
            channel = await self.client.get_entity(channel_id)
            print(f"📂 Membackup channel: {channel.title}")
            print(f"🔒 ID Channel: {channel_id}")
            
            media_count = 0
            total_messages = 0
            failed_count = 0
            
            async for message in self.client.iter_messages(channel):
                total_messages += 1
                
                if message.media:
                    try:
                        file_ext = self.get_file_extension(message)
                        if not file_ext:
                            continue
                            
                        # Buat nama file yang lebih informatif
                        timestamp_msg = message.date.strftime("%Y%m%d_%H%M%S")
                        filename = f"{timestamp_msg}_{message.id}{file_ext}"
                        filepath = os.path.join(backup_folder, filename)
                        
                        print(f"⬇️ Downloading [{media_count + 1}]: {filename}")
                        
                        result = await self.safe_download(message, filepath)
                        if result:
                            media_count += 1
                            print(f"✅ Berhasil: {filename}")
                        else:
                            failed_count += 1
                            print(f"❌ Gagal: {filename}")
                            
                    except Exception as e:
                        failed_count += 1
                        print(f"⚠️ Skip message {message.id}: {str(e)}")
                        continue
                
                # Progress update
                if total_messages % 10 == 0:
                    print(f"📊 Progress: {total_messages} messages | {media_count} sukses | {failed_count} gagal")
            
            # Final report
            print(f"\n🎉 BACKUP SELESAI!")
            print(f"📁 Lokasi: {os.path.abspath(backup_folder)}")
            print(f"📊 Total messages: {total_messages}")
            print(f"✅ Media berhasil: {media_count}")
            print(f"❌ Media gagal: {failed_count}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("💡 Cek: Apakah ID channel benar? Apakah Anda member channel tersebut?")
    
    async def backup_by_username(self, channel_username):
        """Backup channel menggunakan username (untuk channel public)"""
        download_path = "./download"
        os.makedirs(download_path, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(download_path, f"backup_{timestamp}")
        os.makedirs(backup_folder, exist_ok=True)
        
        print(f"📁 Menyimpan file di: {os.path.abspath(backup_folder)}")
        
        try:
            channel = await self.client.get_entity(channel_username)
            print(f"📂 Membackup channel: {channel.title}")
            
            media_count = 0
            total_messages = 0
            
            async for message in self.client.iter_messages(channel):
                total_messages += 1
                
                if message.media:
                    try:
                        file_ext = self.get_file_extension(message)
                        if not file_ext:
                            continue
                            
                        filename = f"media_{message.id}_{total_messages}{file_ext}"
                        filepath = os.path.join(backup_folder, filename)
                        
                        print(f"⬇️ Downloading [{media_count + 1}]: {filename}")
                        
                        result = await self.safe_download(message, filepath)
                        if result:
                            media_count += 1
                            print(f"✅ Berhasil: {filename}")
                        else:
                            print(f"❌ Gagal: {filename}")
                            
                    except Exception as e:
                        print(f"⚠️ Skip message {message.id}: {str(e)}")
                        continue
                
                if total_messages % 10 == 0:
                    print(f"📊 Progress: {total_messages} messages | {media_count} media")
            
            print(f"\n🎉 BACKUP SELESAI!")
            print(f"📁 Lokasi: {os.path.abspath(backup_folder)}")
            print(f"📊 Total: {total_messages} messages | {media_count} media")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    def get_file_extension(self, message):
        """Determine file extension safely"""
        try:
            if hasattr(message.media, 'photo'):
                return ".jpg"
            elif hasattr(message.media, 'document'):
                mime_type = getattr(message.media.document, 'mime_type', '')
                if 'video' in mime_type:
                    return ".mp4"
                elif 'image' in mime_type:
                    return ".jpg"
                elif 'audio' in mime_type:
                    return ".mp3"
                else:
                    # Untuk file tanpa mime type yang jelas
                    return ".dat"
            return None
        except:
            return None
    
    async def safe_download(self, message, filepath):
        """Download dengan error handling"""
        try:
            downloaded_path = await message.download_media(file=filepath)
            return downloaded_path is not None
        except Exception as e:
            print(f"Download error: {e}")
            return False
    
    async def disconnect(self):
        await self.client.disconnect()
        print("🔒 Disconnected")

async def main():
    # === CONFIGURASI ===
    API_ID = xxxx                   # Change Your API ID                    
    API_HASH = "xxxxxx"             # Chage Your API HASH
    PHONE_NUMBER = "+xxxx"          # Change You Phone Number Fromat International
    
    backup = TelegramBackupPrivate(API_ID, API_HASH, PHONE_NUMBER)
    
    try:
        await backup.connect()
        
        print("🔍 Pilih metode backup:")
        print("1. List semua chat/channel dulu")
        print("2. Backup dengan ID channel")
        print("3. Backup dengan username")
        
        choice = input("\nPilih opsi (1/2/3): ").strip()
        
        if choice == "1":
            await backup.list_dialogs()
            
            # Setelah list, tanya ID untuk backup
            channel_id = input("\nMasukkan ID channel untuk backup: ").strip()
            if channel_id:
                await backup.backup_by_id(channel_id)
                
        elif choice == "2":
            channel_id = input("Masukkan ID channel: ").strip()
            await backup.backup_by_id(channel_id)
            
        elif choice == "3":
            channel_username = input("Masukkan username channel (contoh: @namachannel): ").strip()
            await backup.backup_by_username(channel_username)
        else:
            print("❌ Pilihan tidak valid")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        await backup.disconnect()

if __name__ == "__main__":
    print("🚀 Starting Telegram Backup untuk Channel Private...")
    asyncio.run(main())