import matplotlib.pyplot as plt
import sqlite3

#///////////////////////////////////////////////////////////////////////////
# Create a pychart of genres of top events in 100 cities
#///////////////////////////////////////////////////////////////////////////
conn = sqlite3.connect('cities.db')
c = conn.cursor()
c.execute("SELECT * FROM events")
events_data = c.fetchall()

event_genres = {}
for event_data in events_data:
    city_id, city_name, state, event_name, event_genre, date = event_data
    if event_genre in event_genres:
        event_genres[event_genre] = event_genres[event_genre] + 1
    else:
        event_genres[event_genre] = 1
genres = []
num_genres = []
for key, val in event_genres.items():
    if key == "N/A":
        genres.append("No Events")
    else:
        genres.append(key)
    num_genres.append(val)

plt.figure(figsize=(8, 6))
plt.pie(num_genres, labels=genres, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Genres of Top Events in 100 US Cities')
plt.axis('equal')
plt.show()

#/////////////////////////////////////////////////////////////////
# Graph2
#/////////////////////////////////////////////////////////////////

#/////////////////////////////////////////////////////////////////
# Graph3
#/////////////////////////////////////////////////////////////////