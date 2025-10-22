import asyncio
import os
import sys
from datetime import datetime

# Try alternative approach jika telethon bermasalah
try:
    from telethon import TelegramClient
    from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
except ImportError as e:
    print("❌ Error import Telethon:", e)
    print("📦 Coba install: pip install telethon --upgrade")
    sys.exit(1)

class TelegramBackupFixed:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient(f'session_{phone_number}', api_id, api_hash)
        
    async def connect(self):
        """Connect to Telegram"""
        await self.client.start(phone=self.phone_number)
        print("✅ Berhasil connect ke Telegram!")
        
    async def backup_channel(self, channel_username):
        """Backup semua media dari channel"""
        
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
                        # Simple file naming
                        file_ext = self.get_file_extension(message)
                        if not file_ext:
                            continue
                            
                        filename = f"media_{message.id}_{total_messages}{file_ext}"
                        filepath = os.path.join(backup_folder, filename)
                        
                        print(f"⬇️ Downloading [{media_count + 1}]: {filename}")
                        
                        # Download dengan error handling
                        result = await self.safe_download(message, filepath)
                        if result:
                            media_count += 1
                            print(f"✅ Berhasil: {filename}")
                        else:
                            print(f"❌ Gagal: {filename}")
                            
                    except Exception as e:
                        print(f"⚠️ Skip message {message.id}: {str(e)}")
                        continue
                
                # Progress update
                if total_messages % 10 == 0:
                    print(f"📊 Progress: {total_messages} messages | {media_count} media")
            
            # Final report
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
            return ".dat"
        except:
            return ".dat"
    
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
    CHANNEL_USERNAME = "@xxxx"      # Change Your Channel Username
    
    backup = TelegramBackupFixed(API_ID, API_HASH, PHONE_NUMBER)
    
    try:
        await backup.connect()
        await backup.backup_channel(CHANNEL_USERNAME)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        await backup.disconnect()

if __name__ == "__main__":
    print("🚀 Starting Telegram Backup...")
    asyncio.run(main())