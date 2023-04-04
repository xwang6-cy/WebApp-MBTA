from flask import Flask, render_template, request
import requests

from mbta_helper import find_stop_near

app = Flask(__name__)

# Replace YOUR_API_KEY with your actual API key from OpenWeatherMap
API_KEY = "ae7ff952ade6ca145a23e200804aeb94"

def get_weather(place_name):
    # Make a request to the OpenWeatherMap API to get the weather for the given location
    url = f'https://api.openweathermap.org/data/2.5/weather?q={place_name}&units=metric&appid={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the response to get the temperature and weather description
        data = response.json()
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        return temperature, weather_description
    else:
        return None, None

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        place_name = request.form['place_name']
        station_name, is_accessible = find_stop_near(place_name)
        temperature, weather_description = get_weather(place_name)
        if station_name and temperature is not None and weather_description is not None:
            return render_template('result.html',
                                   place_name=place_name,
                                   station_name=station_name,
                                   is_accessible=is_accessible,
                                   temperature=temperature,
                                   weather_description=weather_description)
        else:
            return render_template('error.html')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)




