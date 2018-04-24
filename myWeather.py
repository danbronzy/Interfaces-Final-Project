import geocoder
import requests
import datetime

def getWeather():
    weatherAPI = '0181f5a522583b067ea4da03d5277fea'
    g = geocoder.ip('me')
    str(g.lat)
    stuff = {'APPID':weatherAPI,'lat':g.lat, 'lon':g.lng}

    #weather codes: https://openweathermap.org/weather-conditions
    currWeather = requests.get('http://api.openweathermap.org/data/2.5/weather', params = stuff).json()
    #https://openweathermap.org/current#parameter
    iconID = currWeather['weather'][0]['icon']
    temp = str(int(1.8*(currWeather['main']['temp']-273) + 32)) #degrees f
    cloudCov = str(currWeather['clouds']['all']) #%
    mainWeather = currWeather['weather'][0]['main']
    weatherDescript = currWeather['weather'][0]['description']
    conditions = '%(main)s: %(descript)s' % {'main': mainWeather, 'descript': weatherDescript}
    time = datetime.datetime.fromtimestamp(currWeather['dt']).strftime('%m-%d %I:%M')

    weatherData = []
    weatherData.append({'temp':temp,'cloud':cloudCov,'conditions':conditions,'time':time, 'iconID':iconID})

    forecast = requests.get('http://api.openweathermap.org/data/2.5/forecast', params = stuff).json()
    #https://openweathermap.org/forecast5#JSON

    num3HForecasts = 4
    for i in range(num3HForecasts):
        time = datetime.datetime.fromtimestamp(forecast['list'][i]['dt']).strftime('%m-%d %I:%M')
        iconID = forecast['list'][i]['weather'][0]['icon']
        cloudCov = str(forecast['list'][i]['clouds']['all'])
        temp = str(int(1.8*(forecast['list'][i]['main']['temp']-273)+32))
        mainWeather = forecast['list'][i]['weather'][0]['main']
        weatherDescript = forecast['list'][i]['weather'][0]['description']
        conditions = '%(main)s: %(descript)s' % {'main': mainWeather, 'descript': weatherDescript}
        weatherData.append({'temp':temp,'cloud':cloudCov,'conditions':conditions,'time':time,'iconID':iconID})

    return weatherData
