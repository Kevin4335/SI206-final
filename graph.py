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
# Graph2
#/////////////////////////////////////////////////////////////////




#/////////////////////////////////////////////////////////////////
# Graph3
#/////////////////////////////////////////////////////////////////