import requests
import sqlite3

def fetch_us_cities(num_cities):

    url = "http://api.geonames.org/searchJSON"
    
    params = {
        "q": "US",
        "featureClass": "P",
        "maxRows": num_cities,
        "orderby": "population",
        "username": "yousol"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        cities = [item for item in response.json()["geonames"]]
        return cities
    else:
        print("Failed to fetch cities. Status code:", response.status_code)

"""         for i, city in enumerate(cities):
            print(city) """

conn = sqlite3.connect('cities.db')
c = conn.cursor()

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

        c.execute("INSERT OR IGNORE INTO cities (name, state, population) VALUES (?, ?, ?)",
                  (name, state, population))
        city_row_id = c.lastrowid

    num_rows += 25

c.execute('SELECT * FROM cities')
rows = c.fetchall()
for row in rows:
    print(row)

conn.commit()
conn.close()