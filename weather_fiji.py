import os
import requests
import datetime
import pytz

# Config
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
API_KEY = os.getenv("WEATHER_API_KEY")
FIJI_TZ = pytz.timezone("Pacific/Fiji")

LOCATIONS = [
    {"name": "Suva City", "lat": -18.1416, "lon": 178.4419},
    {"name": "Narere", "lat": -18.0833, "lon": 178.5167},
    {"name": "Khalsa Road", "lat": -18.1000, "lon": 178.4667}
]

def get_weather(lat, lon):
    # Using forecast endpoint to get 'pop' (probability of precipitation)
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&cnt=1"
    try:
        r = requests.get(url).json()
        data = r['list'][0]
        return {
            "temp": round(data['main']['temp']),
            "desc": data['weather'][0]['description'].capitalize(),
            "rain": round(data.get('pop', 0) * 100),
            "wind": round(data['wind']['speed'] * 3.6), # Convert m/s to km/h
            "hum": data['main']['humidity']
        }
    except:
        return None

def send_update():
    now = datetime.datetime.now(FIJI_TZ)
    time_str = now.strftime("%I:%M %p")
    
    embed_fields = []
    extreme_wind = False
    
    for loc in LOCATIONS:
        w = get_weather(loc['lat'], loc['lon'])
        if w:
            if w['wind'] >= 50: extreme_wind = True
            
            field_val = (f"🌡️ {w['temp']}°C | ☁️ {w['desc']}\n"
                         f"☔ Rain: {w['rain']}% | 💨 Wind: {w['wind']} km/h")
            embed_fields.append({"name": f"📍 {loc['name']}", "value": field_val, "inline": False})

    # Discord Webhook Payload
    payload = {
        "content": "@everyone ⚠️ **HIGH WIND ALERT**" if extreme_wind else "",
        "embeds": [{
            "title": f"🇫🇯 Fiji Weather Update - {time_str}",
            "description": f"Detailed report for {now.strftime('%A, %d %B %Y')}",
            "color": 3447003, # Blue color
            "fields": embed_fields,
            "footer": {"text": "Data: OpenWeatherMap | Fiji Meteorological Service"}
        }]
    }
    
    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    send_update()
