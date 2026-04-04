#API openweathermap не работает (не войти в аккаунт), так что сделал свой варик со стимом
#если будет надо, то переделаю на owm, используя другие 3 буквы

import requests
import json

city_name = input('enter city name: ') or 'London'
key = '2f44ab8d94825710392977b37c24d3ac' #стереть перед пушем
response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key}')
result = json.loads(response.text)
if response.status_code == 200:
    weather = result['weather'][0]['description']
    main = result['main']
    
    print(f'Current weather in {city_name}: {weather}')
    print(f'Temperature: {main['temp'] - 273.15}°C')
    print(f'Pressure: {main['pressure']} hPa')
else:
    print(f"Error: {result.get('message', 'Unknown error')}")


#TACKA 2


API_KEY = 'B480F8729281CAF6C4B94A475BE7A6B4' #сотру перед пушем если че
user_steamid = input('user steamid: ') or '76561198917524057'

def getUserOwnedGames(user_steamid):
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        'format' : 'json',
        'key' : API_KEY,
        'include_appinfo' : '1',
        'include_played_free_games' : '1',
        'include_free_sub' : '1',
        'steamid' : user_steamid,
    }
    response = requests.get(url=url, params=params)

    return response.json()

result = getUserOwnedGames(user_steamid)['response']
games_count = result['game_count']
games_list = []

print('data for userid: ', user_steamid)
print('total games owned: ', games_count)
print('owned games list:')

for i in result['games']:
    currentgame = i['name']
    games_list.append(currentgame)
    print(currentgame)

#tkinter не обязательно!!!
#pqt