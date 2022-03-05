import json
import requests
from slack_bolt import App
import os

'''
#https://slack.dev/bolt-python/tutorial/getting-started
#https://slack.dev/bolt-python/concepts

#export SLACK_BOT_TOKEN=xoxb-<your-bot-token>
#export SLACK_APP_TOKEN=<your-app-level-token>
'''

app = App(token=os.environ['SLACK_BOT_TOKEN'], signing_secret=os.environ['SLACK_APP_TOKEN'])

'''
@app.command("/jumo_weather")
def slack_command(ack, respond, command, body):
    # Acknowledge command request
    ack()
    print(body)
    respond(f"{command['text']}")
'''


@app.command("/jumo_weather")
def jumo_weather(ack, body):
    city = body['text']
    weather = get_coordinates(city)  # Execute weather api to get coordinates of City.
    if len(weather.text) > 2:
        coordinates_json = json.loads(weather.text)
        lat = coordinates_json[0]['lat']
        lon = coordinates_json[0]['lon']
        jumo_weather_results = get_city_weather(lat, lon)  # Execute API call to get weather results from coordinates.
        city_weather = json.loads(jumo_weather_results.text)
        user_id = body["user_id"]
        ack(f"Hi <@{user_id}>! Here are your results for {city_weather['name']}, "
            f"{city_weather['sys']['country']}: "
            f"{city_weather['weather'][0]['description']} "
            f"and the temperature is: {round(city_weather['main']['temp'] - 273.15)}C."
            f" The wind speed is: {city_weather['wind']['speed']}")
    else:
        ack("Invalid City. Please retry your request!")


def get_coordinates(city, weather_api=os.environ['openweathermap']):
    r = requests.get(url='http://api.openweathermap.org/geo/1.0/direct',
                     params={'q': city, 'appid': weather_api})
    return r


def get_city_weather(lat, lon, weather_api=os.environ['openweathermap']):
    r = requests.get(url='http://api.openweathermap.org/data/2.5/weather',
                     params={'lat': lat, 'lon': lon, 'appid': weather_api})
    return r


if __name__ == "__main__":
    app.start(3000)  # POST http://localhost:3000/slack/eventsl
