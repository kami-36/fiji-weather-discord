import requests
import datetime
import pytz

WEBHOOK_URL = "https://discord.com/api/webhooks/1456627542306848789/I0sYkn2slmLWOEmqWrfYT4vBp6Su1zsbMHGAIdgNTS_qHibyS8F8JEWznxccBZg-WZsj"

FIJI_TZ = pytz.timezone("Pacific/Fiji")

def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})

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
    page = requests.get("https://www.met.gov.fj").text.lower()
    keywords = ["cyclone", "warning", "alert", "tropical"]

    if any(k in page for k in keywords):
        send(
            "🚨 **WEATHER ALERT – FIJI**\n"
            "Possible cyclone or severe warning issued.\n"
            "👉 Check official site immediately:\n"
            "https://www.met.gov.fj"
        )

now = datetime.datetime.now(FIJI_TZ)

# 7 AM daily message
if now.hour == 7:
    daily_weather()

# Always check for cyclone alerts
cyclone_check()
