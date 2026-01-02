import os
import requests
import datetime
import pytz

# Securely fetch the webhook URL from GitHub Secrets
WEBHOOK_URL = os.getenv("WEBHOOKDISCORDWEATHER")

FIJI_TZ = pytz.timezone("Pacific/Fiji")

def send(msg):
    if not WEBHOOK_URL:
        print("Error: DISCORD_WEBHOOK environment variable is not set.")
        return
    
    try:
        response = requests.post(WEBHOOK_URL, json={"content": msg})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message to Discord: {e}")

def daily_weather():
    today = datetime.datetime.now(FIJI_TZ).strftime("%A, %d %B %Y")
    msg = (
        f"🌤 **Daily Weather – Fiji**\n"
        f"📅 {today}\n\n"
        f"Check official forecast:\n"
        f"https://www.met.gov.fj"
    )
    send(msg)

def cyclone_check():
    # Simple check using FMS homepage
    try:
        page = requests.get("https://www.met.gov.fj", timeout=10).text.lower()
        keywords = ["cyclone", "warning", "alert", "tropical"]

        if any(k in page for k in keywords):
            send(
                "🚨 **WEATHER ALERT – FIJI**\n"
                "Possible cyclone or severe warning issued.\n"
                "👉 Check official site immediately:\n"
                "https://www.met.gov.fj"
            )
    except Exception as e:
        print(f"Error checking FMS website: {e}")

# Get current time in Fiji
now = datetime.datetime.now(FIJI_TZ)

# 7 AM daily message (Fiji Time)
if now.hour == 7:
    daily_weather()

# Always check for cyclone alerts
cyclone_check()
