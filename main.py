import sqlite3
import time
import requests
import json
from datetime import datetime

with open("config.json") as f:
    config = json.load(f)
API_KEY = config["airvisual_api_key"]


# Initialize SQLite database
def initialize_db():
    conn = sqlite3.connect('air_quality.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS air_quality_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        aqi INTEGER,
        temperature INTEGER,
        humidity INTEGER
        )''')
    conn.commit()
    conn.close()


def fetch_air_quality(city, state, country):
    API_URL = "http://api.airvisual.com/v2/city"
    params = {
        'city': city,
        'state': state,
        'country': country,
        'key': API_KEY
    }

    response = requests.get(API_URL, params=params)
    current_date = datetime.now().strftime('%Y-%m-%d')

    if response.status_code == 200:
        try:
            data = json.loads(response.text)['data']
            print(f"Successfully fetched data for {city}, {state}, {country} on {current_date}.")
            return {
                'date': current_date,
                'city': city,
                'state': state,
                'country': country,
                'aqi': data['current']['pollution']['aqius'],
                'temperature': data['current']['weather']['tp'],
                'humidity': data['current']['weather']['hu']
            }
        except KeyError:
            print("Unexpected API response format")
            print(response.text)
            return None
    elif response.status_code == 429:
        print("Rate limit reached. Retrying in 60 seconds...")
        time.sleep(60)
        return fetch_air_quality(city, state, country)
    elif response.status_code == 400:
        print("Bad request. Skipping this city.")
        return None
    else:
        print(f"Failed to get data. Status Code: {response.status_code}")
        print(response.text)
        return None


# Store air quality data into SQLite database
def store_data(data):
    conn = sqlite3.connect('air_quality.db')
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO air_quality_data (date, city, state, country, aqi, temperature, humidity) VALUES "
        f"('{data['date']}', '{data['city']}', '{data['state']}', '{data['country']}', {data['aqi']}, {data['temperature']}, {data['humidity']})"
    )
    conn.commit()
    conn.close()

def print_row(rows):
    print("Database contents:")
    print("ID | Date        | City            | State       | Country         | AQI  | Temperature (C)| Humidity")
    print("-----------------------------------------------------------------------------------------------------")

    for row in rows:
        id_str = str(row[0])[:3]
        date_str = row[1][:10]
        city_str = row[2][:14]
        state_str = row[3][:11]
        country_str = row[4][:16]
        aqi_str = str(row[5])[:4]
        temp_str = str(row[6])[:14]
        humidity_str = str(row[7])[:8]

        print(
            f"{id_str:<3} | {date_str:<10} | {city_str:<14} | {state_str:<11} | {country_str:<16} | {aqi_str:<4} | {temp_str:<14} | {humidity_str:<8}")

# Print the SQLite database
def print_database():
    conn = sqlite3.connect('air_quality.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM air_quality_data")
    rows = cursor.fetchall()
    print_row(rows)
    conn.close()

def print_sorted_by_date():
    conn = sqlite3.connect('air_quality.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM air_quality_data ORDER BY date ASC")
    rows = cursor.fetchall()
    print_row(rows)
    conn.close()

def print_sorted_by_aqi():
    conn = sqlite3.connect('air_quality.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM air_quality_data ORDER BY aqi ASC")
    rows = cursor.fetchall()
    print_row(rows)
    conn.close()

def print_sorted_by_temp():
    conn = sqlite3.connect('air_quality.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM air_quality_data ORDER BY temperature DESC")
    rows = cursor.fetchall()
    print_row(rows)
    conn.close()

def print_sorted_by_humidity():
    conn = sqlite3.connect('air_quality.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM air_quality_data ORDER BY humidity DESC")
    rows = cursor.fetchall()
    print_row(rows)
    conn.close()

def print_sorted_by_state_and_city():
    conn = sqlite3.connect('air_quality.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM air_quality_data ORDER BY state ASC, city ASC")
    rows = cursor.fetchall()
    print_row(rows)
    conn.close()

# delete database
def delete_all_records():
    conn = sqlite3.connect('air_quality.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM air_quality_data")
    conn.commit()
    conn.close()

def run_fetch(city_list):
    for city_info in city_list:
        data = fetch_air_quality(city_info['city'], city_info['state'], city_info['country'])
        if data:
            store_data(data)
        else:
            print(f"Failed to fetch data for {city_info['city']}, {city_info['state']}, {city_info['country']}")


#// it can only run five a time before having to wait for a cool down
if __name__ == "__main__":
    initialize_db()

    city_list = [
        {'city': 'Los Angeles', 'state': 'California', 'country': 'USA'},
        {'city': 'New York City', 'state': 'New York', 'country': 'USA'},
        {'city': 'London', 'state': 'England', 'country': 'United Kingdom'},
        {'city': 'St. Louis', 'state': 'Missouri', 'country': 'USA'},
        {'city': 'Chicago', 'state': 'Illinois', 'country': 'USA'},
        {'city': 'Houston', 'state': 'Texas', 'country': 'USA'},
        {'city': 'San Francisco', 'state': 'California', 'country': 'USA'},
        {'city': 'Miami', 'state': 'Florida', 'country': 'USA'},
        {'city': 'Tokyo', 'state': 'Tokyo', 'country': 'Japan'},
        {'city': 'Berlin', 'state': 'Berlin', 'country': 'Germany'},
        {'city': 'Sydney', 'state': 'New South Wales', 'country': 'Australia'},
        {'city': 'Toronto', 'state': 'Ontario', 'country': 'Canada'},
        {'city': 'Mumbai', 'state': 'Maharashtra', 'country': 'India'},
        {'city': 'Paris', 'state': 'Île-de-France', 'country': 'France'},
        {'city': 'Beijing', 'state': 'Beijing', 'country': 'China'},
        {'city': 'Johannesburg', 'state': 'Gauteng', 'country': 'South Africa'},
        {'city': 'Moscow', 'state': 'Moscow', 'country': 'Russia'},
        {'city': 'Mexico City', 'state': 'Mexico City', 'country': 'Mexico'},
        {'city': 'Buenos Aires', 'state': 'Buenos Aires', 'country': 'Argentina'},
    ]

    run_fetch(city_list = city_list)
    
    # delete_all_records() #to delete table

    # print_database()