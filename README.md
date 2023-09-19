# SkyWatch


This Python script fetches and stores air quality data from different cities around the world into an SQLite database.

## Table of Contents
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Features](#features)
- [Functions](#functions)
    - [`initialize_db()`](#initialize_db)
    - [`fetch_air_quality(city, state, country)`](#fetch_air_qualitycity-state-country)
    - [`store_data(data)`](#store_datadata)
    - [`print_row(rows)`](#print_rowrows)
    - [`print_database()` and Sorting Functions](#print_database-and-sorting-functions)
    - [`delete_all_records()`](#delete_all_records)

## Dependencies

- `sqlite3`
- `time`
- `requests`
- `json`
- `datetime`

## Configuration

Before running the script, make sure you have a `config.json` file with the AirVisual API key:

\```json
{
  "airvisual_api_key": "YOUR_API_KEY"
}
\```

## Features

- Initialize SQLite database with a specific schema.
- Fetch air quality data from an API.
- Store the fetched data into the SQLite database.
- Various functions for viewing the database.
- Supports rate limiting and retries.

## Functions

### `initialize_db()`

Initializes an SQLite database with a specific table schema for storing air quality data.

### `fetch_air_quality(city, state, country)`

Fetches air quality data for a specific location from the API. The function returns this data as a dictionary. It also handles various types of API errors and rate limiting.

### `store_data(data)`

Takes a dictionary containing air quality data and stores it in the SQLite database.

### `print_row(rows)`

A utility function that takes a list of database rows and pretty-prints them to the console.

### `print_database()` and Sorting Functions

These functions are responsible for displaying the database contents. They allow the user to view data sorted by different attributes, such as date, AQI, temperature, and humidity.

- `print_database()`
- `print_sorted_by_date()`
- `print_sorted_by_aqi()`
- `print_sorted_by_temp()`
- `print_sorted_by_humidity()`
- `print_sorted_by_state_and_city()`

### `delete_all_records()`

Deletes all records from the database. Use this function with caution as it will remove all stored data.





