import os
import requests
import datetime
import pytz

# Securely fetch the webhook and API key
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

FIJI_TZ = pytz.timezone("Pacific/Fiji")

def send_to_discord(content=None, embed=None):
    payload = {}
    if content: payload["content"] = content
    if embed: payload["embeds"] = [embed]
    
    if not WEBHOOK_URL:
        print("CRITICAL: Discord Webhook Secret is missing!")
        return

    r = requests.post(WEBHOOK_URL, json=payload)
    print(f"Discord Response: {r.status_code}")

def get_weather():
    # Testing with Suva coordinates
    url = f"https://api.openweathermap.org/data/2.5/weather?lat=-18.1416&lon=178.4419&appid={WEATHER_API_KEY}&units=metric"
    
    if not WEATHER_API_KEY:
        return "ERROR: WEATHER_API_KEY secret is missing in GitHub!"

    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            return f"ERROR: OpenWeather API says: {data.get('message', 'Unknown Error')}"

        temp = round(data['main']['temp'])
        desc = data['weather'][0]['description'].capitalize()
        
        return {
            "title": "🇫🇯 Fiji Weather Test",
            "description": f"Successfully connected! \n📍 **Suva City**\n🌡️ **Temp:** {temp}°C\n☁️ **Conditions:** {desc}",
            "color": 3066993 # Green
        }
    except Exception as e:
        return f"ERROR: Script crashed with: {str(e)}"

# RUN THE TEST
result = get_weather()

if isinstance(result, str):
    # If result is a string, it's an error message
    send_to_discord(content=f"🚨 **Bot Troubleshooting:** {result}")
else:
    # If result is a dictionary, it's a successful embed
    send_to_discord(embed=result)
