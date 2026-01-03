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
    # Forecast endpoint for rain probability
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&cnt=1"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        
        if r.status_code != 200:
            return f"API Error: {data.get('message', 'Invalid Key')}"
            
        item = data['list'][0]
        return {
            "temp": round(item['main'].get('temp', 0)),
            "desc": item['weather'][0].get('description', 'Clear').capitalize(),
            "rain": round(item.get('pop', 0) * 100),
            "wind": round(item['wind'].get('speed', 0) * 3.6),
            "hum": item['main'].get('humidity', 0)
        }
    except Exception as e:
        return f"Error: {str(e)}"

def send_update():
    now = datetime.datetime.now(FIJI_TZ)
    time_str = now.strftime("%I:%M %p")
    
    embed_fields = []
    extreme_wind = False
    error_detected = None
    
    for loc in LOCATIONS:
        w = get_weather(loc['lat'], loc['lon'])
        
        if isinstance(w, dict):
            if w['wind'] >= 50: extreme_wind = True
            field_val = (f"🌡️ {w['temp']}°C | ☁️ {w['desc']}\n"
                         f"☔ Rain: {w['rain']}% | 💨 Wind: {w['wind']} km/h")
        else:
            error_detected = w # Capture the API error message
            field_val = f"⚠️ {w}"
            
        embed_fields.append({"name": f"📍 {loc['name']}", "value": field_val, "inline": False})

    payload = {
        "content": "@everyone ⚠️ **HIGH WIND ALERT**" if extreme_wind else "",
        "embeds": [{
            "title": f"🇫🇯 Fiji Weather Update - {time_str}",
            "description": f"Report for {now.strftime('%A, %d %B %Y')}",
            "color": 15158332 if error_detected else 3447003, # Red if error, Blue if OK
            "fields": embed_fields,
            "footer": {"text": "FMS & OpenWeather | Updates: 7am, 12pm, 5pm, 9pm"}
        }]
    }
    
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    send_update()
