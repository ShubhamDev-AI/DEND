import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS song_table"
artist_table_drop = "DROP TABLE IF EXISTS artist_table"
time_table_drop = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    PRIMARY KEY (event_id),
    artist VARCHAR(255),
    auth VARCHAR(255),
    firstName VARCHAR(50),
    gender VARCHAR(1),
    itemInSession	VARCHAR(255),
    lastName	VARCHAR(50),
    length	VARCHAR(255),
    level	VARCHAR(255),
    location	VARCHAR(255),
    method	VARCHAR(255),
    page	VARCHAR(255),
    registration	VARCHAR(255),
    sessionId	VARCHAR(255),
    song	VARCHAR(255),
    status	INTEGER,
    ts	BIGINT,
    userAgent	VARCHAR(255),
    userId VARCHAR(255)
);""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs INTEGER,
    artist_id VARCHAR(255),
    artist_latitude VARCHAR(255),
    artist_longitude VARCHAR(255),
    artist_location VARCHAR(100),
    artist_name VARCHAR(100),
    song_id VARCHAR(255),
    title VARCHAR(255),
    duration float,
    year int
);""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id SERIAL PRIMARY KEY, 
    start_time time NOT NULL, 
    user_id VARCHAR(255) NOT NULL, 
    level VARCHAR(255), 
    song_id VARCHAR(255) NOT NULL, 
    artist_id VARCHAR(255) NOT NULL, 
    session_id VARCHAR(255), 
    location VARCHAR(255), 
    user_agent VARCHAR(255)
);""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY, 
    first_name VARCHAR(255),
    last_name VARCHAR(255), 
    gender VARCHAR(255),
    level VARCHAR(255),
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR(255) PRIMARY KEY, 
    title VARCHAR(255), 
    artist_id VARCHAR(255) NOT NULL, 
    year INTEGER, 
    duration FLOAT NOT NULL
);""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR(255) PRIMARY KEY, 
    name VARCHAR(255),
    location VARCHAR(255),
    lattitude VARCHAR(255),
    longitude VARCHAR(255),
);""")


time_table_create = ("""CREATE TABLE time(
    start_time TIMESTAMP NOT NULL,
    hour INTEGER NOT NULL,
    day INTEGER NOT NULL,
    week INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    weekday INTEGER NOT NULL,
    PRIMARY KEY (start_time))
""")

# STAGING TABLES

staging_events_copy = ("""
 copy staging_events from '{}'
    credentials 'aws_iam_role={}'
     region 'us-west-2'
     json '{}'
     maxerror as 100;
""").format(LOG_DATA,ARN, LOG_JSONPATH)

staging_songs_copy = ("""
    copy staging_songs from {}
    credentials iam_role {}
    FORMAT AS JSON 'auto';
""").format(config.get('S3','SONG_DATA'), 
            config.get('IAM_ROLE','ARN'))

# FINAL TABLES
    
song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) 
VALUES (
SELECT DISTINCT song_id, title, artist_id, year, duration 
FROM staging_songs
) 
ON CONFLICT (song_id) DO NOTHING""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, lattitude, longitude) 
VALUES (
SELECT DISTINCT artist_id, artist_name, artist_location, rtist_latitude, artist_longitude
FROM staging_songs
) 
ON CONFLICT (artist_id) DO NOTHING""")

# we only take the most recent data of users from staging_events 
user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level) 
VALUES (
SELECT DISTINCT userId, firstName, lastName, gender, level
FROM (
    SELECT userId, firstName, lastName, gender, level,
    row_number() OVER (PARTITION BY userId ORDER BY ts desc) update_index
    FROM staging_events
    )
WHERE update_index = 1
)  
ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT 
        start_time, 
        EXTRACT(hr from start_time) AS hour,
        EXTRACT(d from start_time) AS day,
        EXTRACT(w from start_time) AS week,
        EXTRACT(mon from start_time) AS month,
        EXTRACT(yr from start_time) AS year, 
        EXTRACT(weekday from start_time) AS weekday 
    FROM (
    	SELECT DISTINCT  TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' as start_time 
        FROM staging_events   
    )
""")

# we only take the most recent data of users from staging_events 
songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
VALUES (
    SELECT DISTINCT
        TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' as start_time , 
        se.userId, se.level, s.song_id, a.artist_id, se.sessionId, se.location, se.userAgent
    FROM (SELECT *, row_number() OVER (PARTITION BY userId ORDER BY ts desc) update_index FROM staging_events WHERE update_index = 1) se 
        LEFT JOIN songs s
        ON s.title = s.song and s.duration = se.length
        LEFT JOIN artists a
        ON s.artist_id = a.artist_id and a.name = se.artist
    WHERE se.page = 'NextSong' and se.update_index=1
) 
ON CONFLICT (songplay_id) DO NOTHING""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert, songplay_table_insert]