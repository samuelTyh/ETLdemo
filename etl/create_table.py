import psycopg2
from sql_queries import create_table_queries, drop_table_queries
import configparser


def drop_tables(cur, conn):
    """
    Execute drop queries
    :param cur: DB cursor
    :param conn: DB connection
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Execute create queries
    :param cur: DB cursor
    :param conn: DB connection
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('config.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()