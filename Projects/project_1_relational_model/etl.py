import os
import glob
import psycopg2
import pandas as pd
import datetime
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Extract songs and artists data from song json files and insert data into songs and artists tables, respectively.
    
    Parameters
    ----------
    cur : object
        Cursor to connect with PostgreSQL
    filepath: path str
        Path which contains files
    """
    
    # open song file
    df = pd.read_json(filepath, lines=True) 

    # insert song record
    song_data = list(df[["song_id", "title", "artist_id", "year", "duration"]].values[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Extract data from log json files, transform time data and insert both time, users and songplays data into time, users and songplays tables.
    
    Parameters
    ----------
    cur : object
        Cursor to connect with PostgreSQL
    filepath: path str
        Path which contains files
    """
    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df["page"]=="NextSong"]

    # convert timestamp column to datetime
    t = df["ts"].apply(lambda x: datetime.datetime.fromtimestamp(x / 1e3))
    
    # insert time data records
    hours = t.apply(lambda x: x.hour)
    days = t.apply(lambda x: x.day)
    weeks = t.apply(lambda x: x.week)
    months = t.apply(lambda x: x.month)
    years = t.apply(lambda x: x.year)
    weekdays = t.apply(lambda x: x.weekday())
    
    time_data = (t, hours, days, weeks, months, years, weekdays)
    column_labels = ("start_time", "hour", "day", "week", "month", "year", "weekday")
    time_df = pd.DataFrame({column_labels[i]: d for i,d in enumerate(time_data)})

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[[ 'userId', "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (datetime.datetime.fromtimestamp(row.ts/1000), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Get files and iterate over them to process data (extract, transform and load).
    
    Parameters
    ----------
    cur : object
        Cursor to connect with PostgreSQL
    conn: object
        Connection to database
    filepath: path str
        Path which contains files
    func: function object
        Function used to process data
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Connect and process data.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()