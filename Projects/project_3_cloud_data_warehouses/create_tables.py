import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """ 
    Remove database tables from drop_table_queries, which contains DROP statements
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """ 
    Create database tables from create_table_queries, which contains INSERT statements
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Create database tables from scratch. If tables already exist, their will be remove and created again with empty values.
    """
    
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    print('Connecting to Redshift')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    print('Droping tables if exist')
    drop_tables(cur, conn)
    
    print('Creating new tables')
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()