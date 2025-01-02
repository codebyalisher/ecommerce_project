from django.shortcuts import render
from .models import WeatherData, StockData
import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_geographic_coordinates(city, api_key):
    """ Get the geographic coordinates (latitude and longitude) of a city using the OpenWeatherMap API. """
    geocoding_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}'
    response = requests.get(geocoding_url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        return None, None

def get_weather_data(city):
    """ Get the current weathe,maps,air,geolocation and lot more api's ,here we are uisng weather for a city using the OpenWeatherMap API.in it we have one call mean subscription based and other one is current plan in which we have
    5 calls per 3 hours, and we have a lot of option to like lat,lon,appid,modes,units,lang,exclude,and we can get the response in json or xml format
    we have daily forecast, hourly forecast, current weather, minute forecast, and we can get the data in different languages,we can also get the historical data and statistical api's  of weather 
    """
    api_key = os.getenv("WEATHER_API_KEY")  # Replace with your actual API key from OpenWeatherMap
    lat, lon = get_geographic_coordinates(city, api_key)
    
    if lat is None or lon is None:
        return {
            'city': city,
            'temperature': None,  # Return None for missing temperature
            'description': 'Location not found'
        }

    # Use the Current Weather API
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()

    # Check if the response contains the expected weather data
    if 'main' in data and 'weather' in data:
        return {
            'city': city,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
    else:
        return {
            'city': city,
            'temperature': None,  # Return None if the data is not available
            'description': 'Data not available'
        }

def weather_view(request):
    if request.method == 'POST':
        city = request.POST['city']
        weather_data = get_weather_data(city)
        WeatherData.objects.create(**weather_data)
    
    # Fetch all weather data entries
    weather_data = WeatherData.objects.all().order_by('-retrieved_at')
    return render(request, 'weather.html', {'weather_data': weather_data})


def get_stock_data(symbol):
    """ Intraday Trending,Daily,Daily Adjusted Trending,Weekly,Weekly Adjusted,Monthly,Monthly Adjusted,these are functins upon providing them in api's we can get the data accoridng to the
    function like hourly,daily,weeklty etc. here each fuction has its own parameters and which are used in it
    they are using the symbol in the api's .
    A stock symbol or ticker is a unique series of letters assigned to a security for trading purposes. Stocks listed on the New York Stock Exchange (NYSE) can have four or fewer letters
    """
    api_key =os.getenv("STOCK_API_KEY")  # Replace with your actual API key from Alpha Vantage
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return {
        'symbol': symbol,
        'price': float(list(data['Time Series (1min)'].values())[0]['1. open'])
    }

def stock_view(request):
    if request.method == 'POST':
        symbol = request.POST['symbol']
        stock_data = get_stock_data(symbol)
        StockData.objects.create(**stock_data)
    stock_data = StockData.objects.all().order_by('-retrieved_at')
    return render(request, 'stock.html', {'stock_data': stock_data})