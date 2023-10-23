from dotenv import load_dotenv
import datetime as dt 
import requests
import os

load_dotenv()
api_key = os.getenv('API_KEY')


def get_data(city, API_key):
    resp = requests.get(f'http://api.openweathermap.org/data/2.5/weather?appid={API_key}&q={city}').json()
    return resp

def get_free_forecast_data(city, count, API_key):
    lat = get_lat_lon_time(city)[0]
    lon = get_lat_lon_time(city)[1]
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt={count}&appid={API_key}').json()
    #print(resp)
    #Geeft enkel (max 5) dagen forecast per 3uur
    return resp


def get_forecast_weather(city, count):
    count = int(count) * 8
    counter = 0
    response = get_free_forecast_data(city, count, api_key)
    #print(count,counter)
    
    
    while counter < count:
        print('\n')
        datum = response['list'][counter]['dt_txt']
        temp_kelvin = response['list'][counter]['main']['temp']
        temp_celcius = kelvin_to_celcius(temp_kelvin)
        feels_like_kelvin = response['list'][counter]['main']['feels_like']
        feels_like_celcius = kelvin_to_celcius(feels_like_kelvin)
        wind_speed = response['list'][counter]['wind']['speed']
        humidity = response['list'][counter]['main']['humidity']
        description = response['list'][counter]['weather'][0]['description']
        # sunrise_time = dt.datetime.utcfromtimestamp(response['list'][counter]['sys']['sunrise'] + response['list'][counter]['timezone'])
        # sunset_time = dt.datetime.utcfromtimestamp(response['list'][counter]['sys']['sunset'] + response['list'][counter]['timezone'])
        print(datum)
        print(f"Temperature in {city}: {temp_kelvin:.2f} Kelvin (Hoogstwaarschijnlijk foutief)")
        print(f"Temperature in {city}: {temp_celcius:.2f}°C")
        print(f"Temperature in {city} feels like: {feels_like_celcius:.2f}°C")
        print(f"Humidity in    {city}: {humidity}%")
        print(f"Wind speed in  {city}: {wind_speed}m/s")
        #print(f"Sun rise in    {city}: {sunrise_time} local time")
        #print(f"Sun sets in    {city}: {sunset_time} local time")
        print(f"The sky in     {city}: {description}")
        counter += 8
        print('\n')
    
    




def get_lat_lon_time(city):
    response = get_data(city, api_key)
    lat = response['coord']['lon']
    lon = response['coord']['lat']
    time = response['dt'] + response['timezone']

    lat_lon_t =[0,0,0]
    lat_lon_t[0]=lat
    lat_lon_t[1]=lon
    lat_lon_t[2]=time # unix 
             #   time = dt.datetime.utcfromtimestamp(response['dt'] + response['timezone'])
    
    return lat_lon_t

def kelvin_to_celcius(kelvin):
    celsius = kelvin - 272.15
    return celsius

def get_current_weather(city):
    response = get_data(city, api_key)
    #datum = response['dt_txt']
    temp_kelvin = response['main']['temp']
    temp_celcius = kelvin_to_celcius(temp_kelvin)
    feels_like_kelvin = response['main']['feels_like']
    feels_like_celcius = kelvin_to_celcius(feels_like_kelvin)
    wind_speed = response['wind']['speed']
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']
    sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
    #print(datum)
    print('\n' "_______________________DATACONTROLE______________________" )

    print(f"Temperature in {city}: {temp_celcius:.2f}°C")
    print(f"Temperature in {city} feels like: {feels_like_celcius:.2f}°C")
    print(f"Humidity in    {city}: {humidity}%")
    print(f"Wind speed in  {city}: {wind_speed}m/s")
    print(f"Sun rise in    {city}: {sunrise_time} local time")
    print(f"Sun sets in    {city}: {sunset_time} local time")
    print(f"The sky in     {city}: {description}")
    print('\n' "_______________________DATACONTROLE______________________" '\n')

'''
data vanaf 1979 beschikbaar
'''
def get_forecast_data(city, count, API_key):
    lat = get_lat_lon_time(city)[0]
    lon = get_lat_lon_time(city)[1]
    time = get_lat_lon_time(city)[2]
    print(time)
    days_count=0
    count = int(count)
    if count > 0:
        while days < count:
            time+=(25*60*60)
            days_count+=1
            resp = requests.get(f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={time}&appid={API_key}').json()
            return resp
        #tijdsverspilling

'''
{'cod': 401, 'message': 'Please note that using One Call 3.0 requires a separate subscription to the One Call by Call plan. Learn more here https://openweathermap.org/price.
 If you have a valid subscription to the One Call by Call plan, but still receive this error, then please see https://openweathermap.org/faq#error401 for more info.'}
'''



if __name__ == "__main__":
    city_name = input("Geef een stad op:")
    days = input("Aantal dagen:")
    get_current_weather(city_name)
    get_forecast_weather(city_name, days)