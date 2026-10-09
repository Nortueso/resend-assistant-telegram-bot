# 🤖 Telegram Assistant Bot

[![Python](https://shields.io)](https://python.org)

[![Aiogram](https://shields.io)](https://github.com)

[![Render Deploy](https://shields.io)](https://render.com)

[![License: MIT](https://shields.io)](https://opensource.org)

A convenient Telegram feedback and contact bot designed for developers, freelancers, and content creators. It acts as your **personal digital assistant**: receiving messages from potential employers, clients, or recruiters and instantly forwarding them to you with the author's contact details.

---

## ✨ Features

* **Privacy & Security:** Keep your personal Telegram account hidden from public portfolios, resumes, and websites.
* **Smart Contact Retrieval:** Automatically extracts the sender's `@username` (or falls back to their `Full Name` if their username is hidden by privacy settings).
* **Media Support:** Seamlessly forwards text, photos, voice messages, documents, and code snippets without any quality loss.
* **Privacy Bypass:** Uses the `send_copy` method to send messages from the bot's own identity, bypassing user-level "Forwarded Message" privacy restrictions.
* **Production Ready:** Pre-configured for seamless deployment to the **Render** free tier using Webhooks.

---

## 🛠 Tech Stack

* **Language:** Python 3.10+
* **Framework:** [aiogram 3.x](https://github.com) (Asynchronous Telegram Bot API framework)
* **Web Server:** aiohttp (for handling incoming Telegram Webhooks)
* **Hosting:** Render (Web Services, Free Tier)

---

## 🚀 Quick Start & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com
cd YOUR_REPOSITORY
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# or
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and populate it with your credentials:
```env
BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ  # From @BotFather
TARGET_CHAT_ID=987654321                         # Your personal Telegram user ID
```

---

## 🌍 Deployment to Render (Free Tier)

This bot is fully optimized for **Webhooks** architecture and ready for automated deployment on Render.

1. Push this codebase to your public or private **GitHub** repository.
2. Sign in to [Render.com](https://render.com) and create a new **Web Service**.
3. Connect your repository and configure the build settings:
   * **Language:** `Python`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `python bot.py`
4. Expand the **Environment Variables** section and add:
   * `BOT_TOKEN` — Your Telegram bot token.
   * `TARGET_CHAT_ID` — Your personal Telegram ID.
5. Click **Create Web Service**. The `RENDER_EXTERNAL_URL` setting will be injected automatically, and the bot will self-register its webhook with Telegram.

> 💡 **Pro Tip:** To prevent the Render free tier from sleeping after 15 minutes of inactivity, set up a free uptime monitor (e.g., [UptimeRobot](https://uptimerobot.com)) to ping your app's live URL periodically.

---

## 📝 License

This project is licensed under the MIT License - feel free to use, modify, and distribute it for both personal and commercial use.

---

### 🤝 Contact & Feedback
If you have any questions or suggestions for improvements, feel free to reach out via the bot itself or open an [Issue](https://github.com).
