# 📱 Telegram → Phone Call Bot

Monitors a Telegram channel for the name **"Mantsa"** and immediately calls **+91 9569288612** via Twilio when detected.

---

## 🏗 How It Works

```
Telegram Channel → Bot → Webhook → FastAPI App → Twilio → 📞 Your Phone
```

1. Someone posts a message in your Telegram channel
2. Telegram sends that message to your bot (via webhook)
3. The app checks if "Mantsa" appears in the message
4. If yes → Twilio calls your phone instantly
5. A 5-minute cooldown prevents repeated calls

---

## 🚀 Setup Guide (Step by Step)

### Step 1 — Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send: `/newbot`
3. Give it a name: e.g. `Mantsa Alert Bot`
4. Give it a username: e.g. `mantsa_alert_bot`
5. BotFather will reply with your **Bot Token** — save it!
   ```
   Example: 7123456789:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

### Step 2 — Add Bot to Your Channel

1. Open your Telegram channel
2. Go to **Channel Settings → Administrators → Add Admin**
3. Search for your bot username (e.g. `@mantsa_alert_bot`)
4. Add it with at least **"Post Messages"** permission
5. ✅ Your bot can now read channel messages

---

### Step 3 — Get Your Twilio Credentials

1. Go to [console.twilio.com](https://console.twilio.com)
2. On the dashboard, find:
   - **Account SID** → starts with `AC...`
   - **Auth Token** → click the eye icon to reveal
3. If you don't have a Twilio number yet:
   - Go to **Phone Numbers → Manage → Buy a Number**
   - Get a number with **Voice** capability
   - ⚠️ For Indian numbers (+91): Go to **Verified Caller IDs** and add +919569288612

---

### Step 4 — Deploy to Railway

#### 4a. Push to GitHub

```bash
cd telegram-call-bot

# Initialize git
git init
git add .
git commit -m "Initial commit — Telegram call bot"

# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/telegram-call-bot.git
git push -u origin main
```

#### 4b. Deploy on Railway

1. Go to [railway.app](https://railway.app) → **Login with GitHub**
2. Click **New Project → Deploy from GitHub repo**
3. Select your `telegram-call-bot` repo
4. Railway will auto-detect Python and start building

#### 4c. Add Environment Variables on Railway

In your Railway project → **Variables** tab, add each of these:

| Variable | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather |
| `TWILIO_ACCOUNT_SID` | From Twilio dashboard |
| `TWILIO_AUTH_TOKEN` | From Twilio dashboard |
| `TWILIO_FROM_NUMBER` | Your Twilio number e.g. `+1XXXXXXXXXX` |
| `YOUR_PHONE_NUMBER` | `+919569288612` |
| `WATCH_NAMES` | `Mantsa` |
| `CALL_COOLDOWN_SECONDS` | `300` |

5. Click **Deploy** → wait for it to go green ✅

#### 4d. Get Your Railway URL

In Railway → your project → **Settings → Networking → Public Domain**

It will look like:
```
https://telegram-call-bot-production-xxxx.up.railway.app
```

Copy this URL — you need it for the next step.

---

### Step 5 — Register the Webhook with Telegram

Run this **one-time** command in your terminal (replace the placeholders):

```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<YOUR_RAILWAY_URL>/webhook"
```

**Example:**
```bash
curl "https://api.telegram.org/bot7123456789:AAHxxx/setWebhook?url=https://telegram-call-bot-production-xxxx.up.railway.app/webhook"
```

You should see:
```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

✅ Your bot is now live and listening!

---

### Step 6 — Test It!

1. Go to your Telegram channel
2. Post a message: `Hello Mantsa, please check this`
3. Your phone (+91 9569288612) should ring within **5–10 seconds**!
4. You'll hear: *"Alert! Your name Mantsa was mentioned in your Telegram channel. The message said: Hello Mantsa, please check this."*

---

## 🧪 Test Locally (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Copy and fill in your secrets
cp .env.example .env
# Edit .env with your actual values

# Run the server
python main.py
```

For local testing with Telegram webhooks, use [ngrok](https://ngrok.com):
```bash
ngrok http 8000
# Copy the https URL and use it in Step 5
```

---

## 📋 Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `WATCH_NAMES` | `Mantsa` | Comma-separated names to watch |
| `CALL_COOLDOWN_SECONDS` | `300` | Seconds between calls (5 min) |
| `TELEGRAM_CHANNEL_ID` | *(blank)* | Restrict to specific channel ID |
| `WEBHOOK_SECRET` | *(blank)* | Optional security token |

---

## 🛠 Troubleshooting

**Bot not receiving messages?**
- Make sure the bot is an **admin** in the channel
- Verify the webhook is set: `curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo`

**Call not going through?**
- Check Twilio has sufficient balance
- For trial accounts: verify +919569288612 in Twilio's Verified Caller IDs
- Check Railway logs for errors

**Getting called too often?**
- Increase `CALL_COOLDOWN_SECONDS` (e.g. `600` for 10 minutes)

---

## 🔒 Security Notes

- Never commit `.env` to GitHub — it's in `.gitignore`
- Use Railway's environment variables UI to store secrets
- Optionally set `WEBHOOK_SECRET` to prevent spoofed requests

---

## 📁 Project Structure

```
telegram-call-bot/
├── main.py              # FastAPI app + webhook handler
├── twilio_caller.py     # Twilio Voice API integration
├── config.py            # Environment variable loader
├── requirements.txt     # Python dependencies
├── Procfile             # Railway start command
├── railway.toml         # Railway deployment config
├── .env.example         # Secrets template (safe to commit)
├── .gitignore           # Keeps .env out of git
└── README.md            # This file
```
