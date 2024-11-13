from flask import Flask, render_template, request
import requests
import json
from datetime import datetime

app = Flask(__name__)

API_KEY = "1dc69ab1d0591a0a638c797fb27f6a6a"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    if request.method == 'POST':
        city = request.form['city']
        # Current weather API call
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        # 5-day forecast API call
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        
        try:
            weather_response = requests.get(weather_url)
            forecast_response = requests.get(forecast_url)
            
            if weather_response.status_code == 200 and forecast_response.status_code == 200:
                weather_data = weather_response.json()
                forecast_data = forecast_response.json()
                
                # Process forecast data to get one reading per day
                daily_forecasts = []
                used_dates = set()
                
                for item in forecast_data['list']:
                    date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                    if date not in used_dates:
                        used_dates.add(date)
                        daily_forecasts.append({
                            'date': datetime.fromtimestamp(item['dt']).strftime('%A'),
                            'temp': round(item['main']['temp']),
                            'description': item['weather'][0]['description'],
                            'icon': item['weather'][0]['icon'],
                            'humidity': item['main']['humidity'],
                            'wind': item['wind']['speed']
                        })
                        if len(daily_forecasts) >= 5:
                            break
                
                forecast_data = daily_forecasts
                
        except requests.RequestException:
            return render_template('index.html', error="Failed to fetch weather data")
    
    return render_template('index.html', weather=weather_data, forecast=forecast_data)

if __name__ == '__main__':
    app.run(debug=True)