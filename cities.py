import requests
import sqlite3
import random

def fetch_us_cities(num_cities):
    """
    Fetches US cities data from the GeoNames API.

    Args:
    - num_cities (int): The number of cities to fetch.

    Returns:
    - list: A list of dictionaries containing city data (name, state, population).
    """

    url = "http://api.geonames.org/searchJSON"
    params = {
        "q": "US",
        "featureClass": "P",
        "maxRows": num_cities,
        "orderby": "population",
        "username": "yousol"
    }
    
    params['startRow'] = random.randint(1, 1000)
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        cities = response.json()["geonames"]
        cities = [city for city in cities if city['population'] > 200000]
        return cities
    else:
        print("Failed to fetch cities. Status code:", response.status_code)


conn = sqlite3.connect('cities.db')
c = conn.cursor()

# create cities table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS cities
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              state TEXT NOT NULL,
              population INTEGER NOT NULL)''')

c.execute("SELECT COUNT(*) FROM cities")
num_rows = c.fetchone()[0]

while num_rows < 100:
    cities = fetch_us_cities(25)

    for city in cities:
        name = city['name']
        state = city['adminCode1']
        population = city['population']

        c.execute("SELECT 1 FROM cities WHERE name = ?", (name,))
        existing_city = c.fetchone()

        if not existing_city:
            c.execute("INSERT INTO cities (name, state, population) VALUES (?, ?, ?)", (name, state, population))
            num_rows += 1


c.execute('SELECT * FROM cities')
rows = c.fetchall()
for row in rows:
    print(row)

conn.commit()
conn.close()