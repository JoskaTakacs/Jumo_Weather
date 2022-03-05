import json
import requests
from slack_bolt import App

'''
#https://slack.dev/bolt-python/tutorial/getting-started
#https://slack.dev/bolt-python/concepts

#export SLACK_BOT_TOKEN=xoxb-<your-bot-token>
#export SLACK_APP_TOKEN=<your-app-level-token>
'''

app = App(token='xoxb-3207131180481-3218659194672-pib508Yfq30Hm08s5HN42D9e',
          signing_secret='1336ff50a8a87e4e60b3da1a488b499d')

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
    print(body)
    city = body['text']
    weather = get_coordinates(city)  # Execute weather api to get coordinates of City.
    if len(weather.text) > 2:
        coordinates_json = json.loads(weather.text)
        lat = coordinates_json[0]['lat']
        lon = coordinates_json[0]['lon']
        jumo_weather_results = get_City_Weather(lat, lon)  # Execute API call to get weather results from coordinates.
        city_weather = json.loads(jumo_weather_results.text)
        user_id = body["user_id"]
        ack(f"Hi <@{user_id}>! Here are your results for {city_weather['name']}, "
            f"{city_weather['sys']['country']}: "
            f"{city_weather['weather'][0]['description']} "
            f"and the temperature is: {round(city_weather['main']['temp'] - 273.15)}C."
            f" The wind speed is: {city_weather['wind']['speed']}")
    else:
        ack("Invalid City. Please retry request your request!")


def get_coordinates(city, weather_api='285dbf4413858239fd0f0f786f9d7013'):
    r = requests.get(url='http://api.openweathermap.org/geo/1.0/direct',
                     params={'q': city, 'appid': weather_api})
    print(r.status_code)
    return r


def get_City_Weather(lat, lon, weather_api='285dbf4413858239fd0f0f786f9d7013'):
    r = requests.get(url='http://api.openweathermap.org/data/2.5/weather',
                     params={'lat': lat, 'lon': lon, 'appid': weather_api})
    print(f"get_City_Weather status_code: {r.status_code}")
    return r


if __name__ == "__main__":
    app.start(3000)  # POST http://localhost:3000/slack/eventsl
