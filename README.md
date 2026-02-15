# 👻 Snapy v.1.0.1

> **Fast, Reliable & Professional Snapchat Streak Restorer**

![Snapy Preview](https://raw.githubusercontent.com/beatsbyluca/snapy/refs/heads/main/assets/preview.png)

---

## 📽️ Demo Video
[![Snapy Demo](https://raw.githubusercontent.com/beatsbyluca/snapy/refs/heads/main/assets/preview.png)](https://raw.githubusercontent.com/beatsbyluca/snapy/refs/heads/main/assets/preview.mp4)

*Click the preview image above to watch the demo video!*

## ✨ Features

- ⚡ **Turbo-Charged Speed**: Selective resource blocking ensures the form loads in seconds, not minutes.
- 👥 **Multi-Friend Support**: Process a list of friends sequentially in a single run.
- 🎨 **Premium UI**: Beautiful ASCII header and color-coded logs powered by `pystyle`.
- 🔐 **Anti-Bot Stealth**: Integrated with `playwright-stealth` to bypass basic detection.
- 🖼️ **CAPTCHA Friendly**: Intelligent resource routing allows CAPTCHA images to load while blocking heavy ads/fonts.
- 🔔 **GUI Notifications**: Get an instant Windows popup notice once a restoration is successful.

---

## 🚀 Quick Start

### 1. Requirements
Ensure you have Python 3.8+ installed, then install the dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configuration
Edit the `config.json` file in the root directory:
```json
{
  "username": "your_snapchat_username",
  "email": "your_email@example.com",
  "phone": "+49123456789",
  "friends": [
    "friend_1",
    "friend_2",
    "friend_3"
  ]
}
```

### 3. Run
Start the engine:
```bash
python restorer.py
```

---

## 🛠️ Built With

* [Playwright](https://playwright.dev/python/) - Browser Automation
* [Pystyle](https://github.com/billythegoat356/pystyle) - Terminal Aesthetics
* [EasyGUI](https://github.com/robertlugg/easygui) - Simple UI Notifications
* [Colorama](https://github.com/tartley/colorama) - Terminal Colors

---

## ⚖️ License & Disclaimer
This tool is for educational purposes only. Use it responsibly and in accordance with Snapchat's Terms of Service.

**Created with ❤️ by Beatsbyluca**
