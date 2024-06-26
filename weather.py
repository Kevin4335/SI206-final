import sqlite3
import requests

def fetch_weather(city_name, state_code):
    """
    Fetches current weather data for a given city and state from the WeatherAPI.

    Args:
    - city_name (str): The name of the city.
    - state_code (str): The state code of the city.

    Returns:
    - dict: A dictionary containing weather information (temperature, condition, wind speed).
    """

    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": "8fca84ca1eeb4364a59221439242004",
        "q": f"{city_name},{state_code}"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["current"]
    else:
        return None

def fetch_astro(city_name, state_code):
    """
    Fetches astronomical data (sunrise and sunset times) for a given city and state from the WeatherAPI.

    Args:
    - city_name (str): The name of the city.
    - state_code (str): The state code of the city.

    Returns:
    - dict: A dictionary containing astronomical information (sunrise, sunset).
    """

    url = "http://api.weatherapi.com/v1/astronomy.json"
    params = {
        "key": "8fca84ca1eeb4364a59221439242004",
        "q": f"{city_name},{state_code}"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["astronomy"]["astro"]
    else:
        return None

conn = sqlite3.connect('cities.db')
c = conn.cursor()

c.execute("SELECT * FROM cities")
cities_data = c.fetchall()

c.execute('''CREATE TABLE IF NOT EXISTS weather
             (city_id INTEGER PRIMARY KEY,
              city_name TEXT,
              state TEXT,
              population INTEGER,
              temperature REAL,
              condition TEXT,
              wind_speed REAL)''')

c.execute('''CREATE TABLE IF NOT EXISTS astro
             (city_id INTEGER PRIMARY KEY,
              city_name TEXT,
              sunrise STRING,
              sunset STRING)''')

c.execute("SELECT COUNT(*) FROM weather")
num_rows = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM astro")
num_rows2 = c.fetchone()[0]

def get_weather_data(cities_data):
    """
    Fetches weather data for multiple cities and inserts it into the weather table in the database.

    Args:
    - cities_data (list): A list of tuples containing city data (city_id, city_name, state, population).

    Returns:
    - None
    """
    for city_data in cities_data:
            city_id, city_name, state, population = city_data
            weather_info = fetch_weather(city_name, state)
            if weather_info:
                temperature = weather_info["temp_c"]
                condition = weather_info["condition"]["text"]
                wind_speed = weather_info["wind_kph"]
                c.execute("INSERT OR IGNORE INTO weather (city_id, city_name, state, population, temperature, condition, wind_speed) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (city_id, city_name, state, population, temperature, condition, wind_speed))

def get_times_data(cities_data):
    """
    Fetches astronomical data for multiple cities and inserts it into the astro table in the database.

    Args:
    - cities_data (list): A list of tuples containing city data (city_id, city_name, state, population).

    Returns:
    - None
    """

    for city_data in cities_data:
            city_id, city_name, state, _ = city_data
            astro_info = fetch_astro(city_name, state)
            if astro_info:
                sunrise = astro_info["sunrise"]
                sunset = astro_info["sunset"]
                c.execute("INSERT OR IGNORE INTO astro (city_id, city_name, sunrise, sunset) VALUES (?, ?, ?, ?)",
                        (city_id, city_name, sunrise, sunset))

get_weather_data(cities_data)
get_times_data(cities_data)

c.execute('SELECT * FROM weather')
rows = c.fetchall()
for row in rows:
    print(row)

c.execute('SELECT * FROM astro')
rows = c.fetchall()
for row in rows:
    print(row)

conn.commit()
conn.close()
