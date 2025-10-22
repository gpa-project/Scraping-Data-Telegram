# Telegram Scraping Tool

A powerful and efficient tool for scraping Telegram messages using Python and Telethon library.

## 📋 Features

- Supports both private and public channel scraping
- Session management for persistent authentication
- Secure message extraction and storage
- Configurable download options
- Cross-platform compatibility

## 🔧 Prerequisites

- Python 3.13.7 or higher
- Telegram API credentials (API ID and API Hash)
- Active Telegram account
- Your Telegram account must be a member of the target channel/group for the scraping process to work properly

## 📦 Dependencies

```
telethon==1.31.0
cryptography==41.0.7
rsa==4.9
pyaes==1.6.1
```

## 🚀 Installation

1. Clone this repository:
```bash
git clone [your-repository-url]
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### For Public Channels
```bash
python run-public.py
```

### For Private Channels
```bash
python run-private.py
```

## 📁 Project Structure

```
.
├── README.md
├── requirements.txt
├── run-private.py      # Script for private channels
├── run-public.py       # Script for public channels
├── download/           # Downloaded media storage
└── *.session          # Telegram session files
```

## ⚠️ Important Notes

- Make sure to comply with Telegram's Terms of Service
- Don't use the tool for spam or harassment
- Keep your API credentials secure
- Handle the scraped data responsibly

## 🔐 Security

- Session files contain sensitive information, keep them secure
- Don't share your API credentials
- Use the tool responsibly and ethically

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
