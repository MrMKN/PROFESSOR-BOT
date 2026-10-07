# 🚀 Mr.Guardian_bot (Optimized for Heroku)

Advanced Telegram Message Forwarding & Cloning Bot with UserBot support, auto-rebranding, anti-ban protection, and duplicate filtering.

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

---

## 🌟 Key Features

- **Public & Private Forwarding:** Forward messages from public channels via Bot, or from private/restricted channels using a connected UserBot (Pyrogram String Session).
- **Auto-Rebranding:** Automatically replaces old channel usernames/links with your target channel (default: `@moviesguardianss`).
- **High Speed with Anti-Flood Protection:** Optimized to ~1.8s delay (~33 msgs/min) with randomized human-like jitter and automated FloodWait backoff to keep accounts safe from bans.
- **Hardware Acceleration:** Native `tgcrypto` support for fast MTProto AES encryption.
- **Auto-Restart & Resume:** Ongoing forwarding jobs resume safely upon Heroku dyno restarts using MongoDB persistence.
- **Duplicate & Type Filtering:** Skip duplicate files, filter by keywords, extensions, or media types.
- **Heroku Ready:** Includes `Procfile`, `runtime.txt`, `app.json`, and `.gitignore` for seamless deployment from GitHub.

---

## 🛠️ Heroku Deployment Guide (from GitHub)

### Method 1: Using the Heroku Dashboard & GitHub

1. **Fork or Push this repository to your GitHub account**:
   - Ensure `.env` is **never committed** (it is already protected in `.gitignore`).
2. **Go to Heroku Dashboard**:
   - Click **New** ➔ **Create new app**.
   - Under the **Deploy** tab, select **GitHub** as the deployment method.
   - Search for your repository and click **Connect**.
3. **Configure Environment Variables (Config Vars)**:
   - Go to **Settings** ➔ **Reveal Config Vars** and add the following keys:

| Config Var | Description | Required | Example |
| :--- | :--- | :--- | :--- |
| `API_ID` | Telegram API ID from [my.telegram.org](https://my.telegram.org) | **Yes** | `17030067` |
| `API_HASH` | Telegram API Hash from [my.telegram.org](https://my.telegram.org) | **Yes** | `df64deb205...` |
| `BOT_TOKEN` | Bot Token from [@BotFather](https://t.me/BotFather) | **Yes** | `8924751186:AAH...` |
| `BOT_OWNER` | Numeric Telegram User ID (from [@userinfobot](https://t.me/userinfobot)) | **Yes** | `8371005605` |
| `DATABASE_URI` | MongoDB Connection URI from [MongoDB Atlas](https://mongodb.com) | **Yes** | `mongodb+srv://user:pass@cluster0...` |
| `DATABASE_NAME` | MongoDB database name | No | `Cluster0` |
| `STRING_SESSION` | Pyrogram String Session for UserBot (starts with `BQED...`) | No | `BQED27MAM...` |
| `CHANNEL_USERNAME` | Target channel username for auto-branding | No | `@moviesguardianss` |
| `FORWARD_SLEEP` | Delay per message in seconds | No | `1.8` |

4. **Deploy & Enable Dyno**:
   - Back in the **Deploy** tab, click **Deploy Branch** (or enable **Automatic Deploys**).
   - Once deployed, go to the **Resources** tab.
   - Enable the **`worker: python3 main.py`** dyno and turn off any unused dynos.

---

### Method 2: Using Heroku CLI

```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create your-forward-bot-app --stack heroku-22

# 3. Set Config Vars
heroku config:set API_ID=17030067
heroku config:set API_HASH=df64deb205933fbe14e50237b5ab68f2
heroku config:set BOT_TOKEN=8924751186:AAH3AK-HEHgig0GfsiNTq5yoLZ3UV5kAbxA
heroku config:set BOT_OWNER=8371005605
heroku config:set DATABASE_URI="mongodb+srv://user:pass@cluster0.mongodb.net/?appName=Cluster0"
heroku config:set DATABASE_NAME=Cluster0
heroku config:set CHANNEL_USERNAME=@moviesguardianss
heroku config:set FORWARD_SLEEP=1.8

# 4. Deploy code
git push heroku main

# 5. Scale worker dyno
heroku ps:scale worker=1

# 6. Check logs
heroku logs --tail
```

---

## 🤖 Bot Commands

```text
/start - Check if the bot is alive
/forward - Start a new forwarding task
/settings - Configure userbot, channels, caption, and filters
/unequify - Remove duplicate media from channels
/stop - Stop ongoing task
/reset - Reset your settings
/restart - Restart server (Owner only)
/broadcast - Broadcast message to all users (Owner only)
```

---

## 🔒 Security Note

- **Never** commit `.env` or `*.session` files to public GitHub repositories.
- If you regenerate a bot token or string session, update your Heroku Config Vars accordingly.
