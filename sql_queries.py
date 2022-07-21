#CREATE TABLES
songplay_table_create = (""" CREATE TABLE IF NOT EXISTS songplay(
    songplay_id serial PRIMARY KEY NOT NULL, 
    start_time  numeric, 
    user_id int, 
    level varchar, 
    song_id varchar, 
    artist_id varchar, 
    session_id int, 
    location varchar, 
    user_agent varchar,
    CONSTRAINT fk_time
        FOREIGN KEY (start_time) REFERENCES time(start_time)
    CONSTRAINT fk_users
        FOREIGN KEY (user_id) REFEERENCES
)

""")

user_table_create = (""" CREATE TABLE IF NOT EXISTS song(
    user_id PRIMARY KEY NOT NULL, 
    first_name varchar,
    last_name varchar, 
    gender varchar, 
    level varchar
)
""")


song_table_create = ("""CREATE TABLE IF NOT EXISTS song(
    song_id varchar PRIMARY KEY NOT NULL, 
    title varchar , 
    artist_id varchar, 
    year int, 
    duration numeric
)
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist(
    artist_id varchar PRIMARY KEY, 
    name varchar, 
    location varchar, 
    latitude numeric, 
    longitude numeric
)
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(
    start_time numeric PRIMARY KEY, 
    hour int, 
    day int, 
    week int, 
    month int,
    year int, 
    weekday int
)
""")

songplay_table_insert = ("""INSERT into songplay(
    songplay_id, start_time, user_id, level, song_id, artist_id, 
    session_id, location, user_agent) values \
        (%s,%s,%s,%s,%s,%s,%s,%s)
)
""")

user_table_insert =("""INSERT into user(user_id, 
first_name, last_name, gender, level) values \
        (%s,%s,%s,%s,%s)
)
""")

song_table_insert = ("""INSERT into song(song_id, title, 
artist_id, year, duration) values \
        (%s,%s,%s,%s, %s)
)
""")

artist_table_insert = ("""INSERT into artist(artist_id, name, 
location, latitude, longitude) values \
        (%s,%s,%s,%s,%s)
)
""")

time_table_insert = ("""INSERT into time(start_time, hour, day, 
week, month, year, weekday) values \
        (%s,%s,%s,%s,%s,%s,%s)
)
""")

# FIND SONGS

song_select = ("""
select a.song_id, b.artist_id
from
songs a  
inner join
artists b
on a.artist_id = b.artist_id
where
a.title = %s and b.name = %s and a.duration = %s
""")

#DROP TABLES
songplay_table_drop = ("""DROP TABLE IF EXIST songplay""")
user_table_drop = ("""DROP TABLE IF EXIST users""")
song_table_drop = ("""DROP TABLE IF EXISTS song""")
artist_table_drop = ("""DROP TABLE IF EXIST artist""")
time_table_drop = ("""DROP TABLE IF EXIST time_table_drop""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, \
artist_table_create, time_table_create,songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, \
artist_table_drop, time_table_drop]