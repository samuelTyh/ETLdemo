import psycopg2
import configparser
import argparse
import pandas
from sql_queries import latest_10_days_average_temperature


def print_latest_daily_temperature():
    """
    Print out 10 latest records of requirement
    :return: table will be printed out in the terminal
    """
    config = configparser.ConfigParser()
    config.read('config.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))
    cur = conn.cursor()

    cur.execute(latest_10_days_average_temperature)

    result = cur.fetchall()
    columns = [des[0] for des in cur.description]

    if not result:
        return ConnectionError("Check DB connection")

    result = pandas.DataFrame(result, columns=columns)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--temp', help="Retrieve the daily temperature table", action='store_true')
    args = parser.parse_args()

    if args.temp:
        print_latest_daily_temperature()
    else:
        raise ValueError("Specify the flag of the table to be retrieved, e.g. --temp")