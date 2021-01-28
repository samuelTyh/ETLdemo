import psycopg2
import configparser
import pandas


def print_latest_daily_temperature():
    """
    Print out 10 latest records of requirement
    :return: table will be printed out in the terminal
    """
    config = configparser.ConfigParser()
    config.read('config.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))
    cur = conn.cursor()

    cur.execute(
        """
        SELECT date, location, temperature_celsius, temperature_fahrenheit
        FROM daily_temperature
        ORDER BY date DESC
        LIMIT 10;
        """
    )

    result = cur.fetchall()
    columns = [des[0] for des in cur.description]

    if not result:
        return ConnectionError("Check DB connection")

    result = pandas.DataFrame(result, columns=columns)
    print(result)


if __name__ == "__main__":
    print_latest_daily_temperature()
