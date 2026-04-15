"""
Location Tracker Telegram Bot
=============================
A public bot that fetches location from Firebase and sends Google Maps link.
Anyone can use /location command - no authentication required.
"""

import telebot
import urllib.request
import json
import os
import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==================== CONFIGURATION ====================
# Set via environment variable: BOT_TOKEN
# Or replace with your bot token below (temporary)
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
FIREBASE_URL = os.environ.get('FIREBASE_URL', 'https://location-tracker-e9cf7-default-rtdb.firebaseio.com/user_location.json')
# ==================== END CONFIGURATION ====================

bot = telebot.TeleBot(BOT_TOKEN)

def get_location_from_firebase():
    """Fetch location from Firebase Realtime Database via REST API"""
    try:
        request = urllib.request.Request(FIREBASE_URL)
        request.add_header('User-Agent', 'LocationBot/1.0')
        
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None

def create_google_maps_link(lat, lng):
    """Create Google Maps URL from coordinates"""
    return f"https://www.google.com/maps?q={lat},{lng}"

def format_timestamp(timestamp):
    """Convert Unix timestamp to readable format"""
    from datetime import datetime
    try:
        dt = datetime.fromtimestamp(timestamp / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return str(timestamp)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handle /start command"""
    user = message.from_user
    welcome_text = f"""
👋 *Welcome to Location Tracker Bot!*

Hello {user.first_name}! 👋

I'm a simple bot that provides real-time location data from a tracked device.

📍 *Available Commands:*
/start - Show this welcome message
/location - Get current device location
/help - Show help information

🔒 *Note:* Location data must be sent from the Android app first!
"""
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def send_help(message):
    """Handle /help command"""
    help_text = """
📖 *Help - Location Tracker Bot*

This bot provides real-time location of a tracked Android device.

*How it works:*
1. The Android app sends location to Firebase every 10 minutes
2. Send /location command to get the latest location
3. I'll reply with a Google Maps link

*Commands:*
/start - Welcome message
/location - Get current location
/help - Show this help

*Note:* This bot is public - anyone can use it!
"""
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['location', 'track', 'gps'])
def send_location(message):
    """Handle /location command - PUBLIC access"""
    user = message.from_user
    print(f"Location request from: {user.first_name} (ID: {user.id})")
    
    # Show typing status
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Fetch location from Firebase
    location_data = get_location_from_firebase()
    
    if location_data and 'lat' in location_data and 'lng' in location_data:
        lat = location_data['lat']
        lng = location_data['lng']
        timestamp = location_data.get('timestamp', 0)
        
        # Create Google Maps link
        maps_link = create_google_maps_link(lat, lng)
        
        # Format response
        response = f"📍 *Current Location Found!*\n\n"
        response += f"🗺️ [View on Google Maps]({maps_link})\n\n"
        response += f"📌 *Coordinates:*\n"
        response += f"`{lat}, {lng}`\n\n"
        
        if timestamp:
            response += f"⏰ *Last Updated:* `{format_timestamp(timestamp)}`"
        
        bot.send_message(
            message.chat.id, 
            response, 
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
    else:
        error_text = """
❌ *Location Not Found*

The device hasn't sent any location data yet.

*Make sure:*
1. Android app is installed and running
2. Location permissions are granted
3. App is sending data to Firebase

Try again in a few minutes!
"""
        bot.reply_to(message, error_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    """Handle unknown commands"""
    bot.reply_to(message, 
                 "Sorry, I didn't understand that. Use /help for available commands.",
                 parse_mode='Markdown')

def main():
    """Main function to start the bot"""
    print("=" * 50)
    print("Location Tracker Bot Starting...")
    print("=" * 50)
    print(f"Bot Token: {BOT_TOKEN[:10]}..." if len(BOT_TOKEN) > 10 else "Bot Token: Not set")
    print(f"Firebase URL: {FIREBASE_URL}")
    print("=" * 50)
    print("Bot is running and listening for commands...")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    # Start polling
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        main()  # Restart on error

if __name__ == "__main__":
    main()
