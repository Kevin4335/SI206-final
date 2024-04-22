import sqlite3
import requests
#ticketmaster api

key = "BekZM5p19sxdHOZVHFu1pguLxpAtSAVJ"
root_url = "https://app.ticketmaster.com/discovery/v2/events.json?size=1&apikey=BekZM5p19sxdHOZVHFu1pguLxpAtSAVJ"


def fetch_event(city_name, state_id):
    
    params = {
        "city":city_name,
        "stateCode":state_id,
        "page":"0",
        "radius" : "20",
    }
    response = requests.get(root_url, params=params)
    return response.json()
    # print(response.json()['_embedded']['events'][0]["name"])
    # print(response.json()['_embedded']['events'][0]["classifications"][0]["segment"]["name"])
    # #print(response.json()['_embedded']['events'][0]["type"])


conn = sqlite3.connect('cities.db')
c = conn.cursor()
c.execute("SELECT * FROM cities")
cities_data = c.fetchall()

c.execute('''CREATE TABLE IF NOT EXISTS events
             (city_id INTEGER PRIMARY KEY,
              city_name TEXT,
              state TEXT,
              event_name TEXT,
              event_genre TEXT,
              date TEXT)''')

for city_data in cities_data:
    city_id, city_name, state, population = city_data
    event_data = fetch_event(city_name,state)
    if "page" in event_data:
        if event_data["page"]["totalElements"] !=0:
            if "_embedded" in event_data:
                event_name = event_data['_embedded']['events'][0]["name"]
                
                if "classifications" in event_data['_embedded']['events'][0]:
                    event_genre = event_data['_embedded']['events'][0]["classifications"][0]["segment"]["name"]
                else:
                    event_genre = "Miscellaneous"
                
                if "localDate" in event_data['_embedded']['events'][0]["dates"]["start"]:               
                    date = event_data['_embedded']['events'][0]["dates"]["start"]["localDate"]
                else:
                    date = "N/A"
            else:
                event_name = "N/A"
                event_genre = "N/A"
                date = "N/A"         
        else:
            event_name = "N/A"
            event_genre = "N/A"
            date = "N/A"
    else:
        event_name = "N/A"
        event_genre = "N/A"
        date = "N/A"
        
    c.execute("INSERT OR IGNORE INTO events (city_id, city_name,state,event_name,event_genre,date) VALUES (?, ?, ?, ?, ?, ?)", (city_id, city_name,state,event_name,event_genre,date))
    conn.commit()
    
conn.close()