import os
import glob
import json
import psycopg2
import configparser
from sql_queries import InsertDWH, DailyTemperature


def process_records_file(cur, filepath: str):
    with open(filepath, 'r') as file:
        data = json.load(file)

    location_data = [value for value in data['location'].values()]
    weather_data = [value for value in data['current'].values()][:4] + \
                   [value for value in data['current'].values()][6:]
    staging_data = location_data + weather_data

    # insert records
    insert = InsertDWH()
    cur.execute(insert.staging_table, staging_data)
    cur.execute(insert.location_table)
    cur.execute(insert.datetime_table)
    cur.execute(insert.current_weather_table)

    # process daily temperature
    daily = DailyTemperature()
    cur.execute(daily.select_daily_temperature)


def process_data(cur, conn, filepath: str, func):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print(F'{num_files} files found in {filepath}')

    # iterate over files and process
    for idx, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print(f'{idx}/{num_files} files processed.')


def main():
    config = configparser.ConfigParser()
    config.read('config.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))
    cur = conn.cursor()

    process_data(cur, conn, filepath='./data', func=process_records_file)

    conn.close()


if __name__ == "__main__":
    main()
