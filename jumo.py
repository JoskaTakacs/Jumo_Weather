import json
import requests
from slack_bolt import App
import os

'''
Export Slack and openweathermap API keys as follows:

export SLACK_BOT_TOKEN=xoxb-<your-bot-token>
export SLACK_APP_TOKEN=<your-app-level-token>
export openweathermap=<your-open-weather-map-token>
'''

try:
    app = App(token=os.environ['SLACK_BOT_TOKEN'], signing_secret=os.environ['SLACK_APP_TOKEN'])
except KeyError:
    print('Please export all api keys')


@app.command("/jumo_weather")  # listen for "/jumo_weather" commands from slack
def jumo_weather(ack, body):
    city = body['text']
    weather = get_coordinates(city)  # Execute weather api to get coordinates of City.
    if len(weather.text) > 2:
        coordinates_json = json.loads(weather.text)
        lat = coordinates_json[0]['lat']
        lon = coordinates_json[0]['lon']
        jumo_weather_results = get_city_weather(lat, lon)  # Execute API calls to get weather results from coordinates.
        city_weather = json.loads(jumo_weather_results.text)
        user_id = body["user_id"]
        ack(f"Hi <@{user_id}>! \nHere are your results for {city_weather['name']}, "
            f"{city_weather['sys']['country']}: "
            f"\nThe weather conditions are: {city_weather['weather'][0]['description']} \n"
            f"\nand the temperature is: {round(city_weather['main']['temp'] - 273.15)}C.\n"
            f"\nThe wind speed is: {city_weather['wind']['speed']}")
    else:
        ack("Invalid City. Please retry your request!")


def get_coordinates(city, weather_api=os.environ['openweathermap']):
    try:
        r = requests.get(url='http://api.openweathermap.org/geo/1.0/direct',
                         params={'q': city, 'appid': weather_api})
        return r
    except ConnectionError:
        print('\nError connecting to http://api.openweathermap.org/geo/1.0/direct\n')


def get_city_weather(lat, lon, weather_api=os.environ['openweathermap']):
    try:
        r = requests.get(url='http://api.openweathermap.org/data/2.5/weather',
                         params={'lat': lat, 'lon': lon, 'appid': weather_api})
        return r
    except ConnectionError:
        print('\nError connecting to http://api.openweathermap.org/data/2.5/weather\n')


if __name__ == "__main__":
    app.start(3000)  # POST http://localhost:3000/slack/events
