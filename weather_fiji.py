import os
import requests
import datetime
import pytz

# Securely fetch the webhook URL from the environment variable
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

FIJI_TZ = pytz.timezone("Pacific/Fiji")

def send(msg):
    if not WEBHOOK_URL:
        print("Error: DISCORD_WEBHOOK environment variable is not set.")
        return
    
    try:
        response = requests.post(WEBHOOK_URL, json={"content": msg})
        response.raise_for_status()
        print("Message sent successfully!")
    except Exception as e:
        print(f"Failed to send: {e}")

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
    try:
        page = requests.get("https://www.met.gov.fj", timeout=10).text.lower()
        keywords = ["cyclone", "warning", "alert", "tropical"]
        if any(k in page for k in keywords):
            send("🚨 **WEATHER ALERT – FIJI**\nPossible cyclone/severe warning. Check: https://www.met.gov.fj")
    except Exception as e:
        print(f"Error checking FMS: {e}")

# MAIN EXECUTION
now = datetime.datetime.now(FIJI_TZ)

# TEST MODE: This will run every time you click "Run Workflow"
print(f"Current Fiji Time: {now.strftime('%H:%M')}")
daily_weather() 

# Once testing is done, replace the daily_weather() line above with:
# if now.hour == 7:
#     daily_weather()

cyclone_check()
