import matplotlib.pyplot as plt
import sqlite3
#///////////////////////////////////////////////////////////////////////////
# Graph1 : Bar Chart of populations vs Average num of events
#///////////////////////////////////////////////////////////////////////////
conn = sqlite3.connect('cities.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS num_events 
    (
        city_id INTEGER PRIMARY KEY,
        city_name TEXT,
        state TEXT,
        population TEXT,
        num_events TEXT
    )
''')

c.execute('''
    INSERT OR IGNORE INTO num_events (city_id, city_name, state, population, num_events)
    SELECT cities.id, cities.name, cities.state, cities.population, events.num_events
    FROM cities
    INNER JOIN events ON cities.id = events.city_id
''')

conn.commit()
c.execute("SELECT * FROM num_events")
events_data = c.fetchall()
c.close()
pop_baskets = {
    "200k-300k": (0, 0),
    "300k-400k": (0, 0),
    "400k-500k": (0, 0),
    "500k-600k": (0, 0),
    "600k-700k": (0, 0),
    "700k-800k": (0, 0),
    ">800k": (0, 0),
}
pops = []
events = []
names = []
for event_data in events_data:
    city_id, city_name, state, population, num_events = event_data
    population = int(population)
    num_events = int(num_events)
    
    
    #Las vegas is a big outlier in terms of population + num_events, so i removed it from the data
    if city_name == "Las Vegas":
        pass
    else:
        pops.append(population)
        events.append(num_events)
        names.append(city_name)
        if population > 200000 and population <= 300000:
            init_tup = pop_baskets["200k-300k"]
            pop_baskets["200k-300k"] = (init_tup[0]+1, init_tup[1]+num_events)
        elif population > 300000 and population <= 400000:
            init_tup = pop_baskets["300k-400k"]
            pop_baskets["300k-400k"] = (init_tup[0]+1, init_tup[1]+num_events)
        elif population > 400000 and population <= 500000:
            init_tup = pop_baskets["400k-500k"]
            pop_baskets["400k-500k"] = (init_tup[0]+1, init_tup[1]+num_events)
        elif population > 500000 and population <= 600000:
            init_tup = pop_baskets["500k-600k"]
            pop_baskets["500k-600k"] = (init_tup[0]+1, init_tup[1]+num_events)
        elif population > 600000 and population <= 700000:
            init_tup = pop_baskets["600k-700k"]
            pop_baskets["600k-700k"] = (init_tup[0]+1, init_tup[1]+num_events)
        elif population > 700000 and population <= 800000:
            init_tup = pop_baskets["700k-800k"]
            pop_baskets["700k-800k"] = (init_tup[0]+1, init_tup[1]+num_events)
        elif population > 800000:
            init_tup = pop_baskets[">800k"]
            pop_baskets[">800k"] = (init_tup[0]+1, init_tup[1]+num_events)

baskets = []
values = []
f = open("baskets_averages.txt", "w")
for key, val in pop_baskets.items():
    baskets.append(key)

    values.append(val[1]/val[0])
    f.write(key+": " +str(val[1]/val[0]) + "\n")
f.close()
    
plt.figure(figsize=(10, 6))
plt.bar(baskets, values, color='green')

plt.xlabel('Population of City')
plt.ylabel('Average Number of Events')
plt.title('City Population and Average Number of Events')

plt.grid(True)
plt.show()


#/////////////////////////////////////////////////////////////////
# Graph2: temperature across cities
#/////////////////////////////////////////////////////////////////


# You must select some data from all of the tables in your database and calculate
# something from that data (20 points). You could calculate the count of how many items
# occur on a particular day of the week or the average of the number of items per day.
# ● You must do at least one database join to select your data for your calculations or
# visualizations (20 points).
# ● Write out the calculated data to a file as text (10 points)


conn = sqlite3.connect('cities.db')
cursor = conn.cursor()

cursor.execute("SELECT city_name, temperature FROM weather")
temperature_data = cursor.fetchall()

cities = []
temp_c = []
temp_f = []
for data in temperature_data:
    cities.append(data[0])
    temp_c.append(data[1])
    farenheit = (data[1] * 9/5) + 32
    temp_f.append(farenheit)

with open('temperature_data.txt', 'w') as file:
    file.write('City\tTemperature (F)\n')
    for i in range(0,len(cities)):
        file.write(f'{cities[i]}\t{temp_f[i]}\n')

# plt.figure(figsize=(10, 6))
# plt.bar(cities, temp_f, color='skyblue')
# plt.xlabel('City')
# plt.ylabel('Temperature (F)')
# plt.title('Temperature Across Cities')
# plt.xticks(rotation=45, ha='right', fontsize = 10)  
# plt.tight_layout()  
# plt.show()


plt.figure(figsize=(12, 6))  
plt.bar(cities, temp_f, color='skyblue', width=0.6)  
plt.xlabel('City')
plt.ylabel('Temperature (F)')
plt.title('Temperature Across Cities')
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.tight_layout()  
plt.show()


conn.close()

#/////////////////////////////////////////////////////////////////
# Graph3: pie chart to show distribution of event genres across different cities

#/////////////////////////////////////////////////////////////////

conn = sqlite3.connect('cities.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT event_genre, COUNT(*) AS genre_count
    FROM events
    GROUP BY event_genre
""")
genre_data = cursor.fetchall()

genres = []
counts = []
for data in genre_data:
    # ignore events that don't have an event genre (don't want this to affect pie)
    if data[0] == "N/A": 
        continue
    else:
        genres.append(data[0])
        counts.append(data[1])


total_events = 0
for count in counts:
    total_events += count

percentages = []
for count in counts:
    percent = (count / total_events) * 100
    percentages.append(percent)

with open('event_genre_percentages.txt', 'w') as file:
    file.write('Event Genre\tPercentage\n')
    for genre, percentage in zip(genres, percentages):
        file.write(f'{genre}\t{percentage:.2f}%\n')

plt.figure(figsize=(8, 8))
plt.pie(percentages, labels=genres, autopct='%1.1f%%', startangle=140)
plt.title('Percentage of Event Genres Across All Cities')
plt.axis('equal') 
plt.show()
conn.close()

#/////////////////////////////////////////////////////////////////
# Graph4: average temperatures of the different states (fahrenheit)
#/////////////////////////////////////////////////////////////////

conn = sqlite3.connect('cities.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT state, temperature
    FROM weather
""")
temperature_data = cursor.fetchall()

state_temps = {}
# state, [temp, temp, temp, ...]

temps = []
for state, temp in temperature_data:
    temp_f = (temp * 9/5) + 32
    if state not in state_temps:
        state_temps[state] = [temp_f]
    else:
        state_temps[state].append(temp_f)

avg_state_temps = {}
for state, temp_list in state_temps.items():
    avg_temp = sum(temp_list) / len(temp_list)
    avg_state_temps[state] = avg_temp

states = list(avg_state_temps.keys())
avg_temps = list(avg_state_temps.values())


with open('avg_state_temp_data.txt', 'w') as file:
    file.write('State\tAverage Temperature (F)\n')
    for k,v in avg_state_temps.items():
        file.write(f'{k}\t{v}\n')

plt.figure(figsize=(10, 6))
plt.bar(states, avg_temps, color='orange')
plt.xlabel('State')
plt.ylabel('Average Temperature (Fahrenheit)')
plt.title('Average Temperatures of Different States')
plt.xticks(rotation=45, ha='right') 
plt.tight_layout()  
plt.show()

conn.close()