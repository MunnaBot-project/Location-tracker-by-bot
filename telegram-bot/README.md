# Location Tracker Telegram Bot

## Setup Instructions

### 1. Create Telegram Bot
1. Open Telegram → Search for @BotFather
2. Send /newbot command
3. Follow instructions to create bot
4. Copy the BOT_TOKEN

### 2. Firebase Setup
1. Go to https://console.firebase.google.com
2. Create new project
3. Build → Realtime Database → Create Database
4. Start in **Test Mode**
5. Copy your PROJECT_ID (shown in project settings)

### 3. Configure Bot
Edit `bot.py` and replace:
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # From BotFather
FIREBASE_URL = "https://YOUR_PROJECT_ID-default-rtdb.firebaseio.com/user_location.json"
```

### 4. Run Bot Locally
```bash
cd telegram-bot
pip install pyTelegramBotAPI requests
python bot.py
```

### 5. Deploy for Free
**Option A: Render**
1. Push code to GitHub
2. Sign up at render.com
3. Create Web Service → Connect GitHub
4. Build: `pip install pyTelegramBotAPI requests`
5. Start: `python bot.py`

**Option B: PythonAnywhere**
1. Sign up at pythonanywhere.com
2. Upload bot.py
3. Terminal: `pip install pyTelegramBotAPI requests`
4. Run: `python bot.py`

---

## Commands
- `/start` - Welcome message
- `/help` - Help
- `/location` - Get current location (PUBLIC - anyone can use)

---

## Android App Setup
1. Download google-services.json from Firebase Console
2. Place in `android/app/google-services.json`
3. Build APK: `cd android && ./gradlew assembleDebug`
4. Install on phone, grant permissions
5. Click "Grant Permissions" button