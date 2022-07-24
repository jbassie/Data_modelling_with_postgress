import os
import glob
from time import time
from tkinter.filedialog import LoadFileDialog
import pandas as pd
import psycopg2
import numpy as np
from pyparsing import line
from sql_queries import *
from datetime import datetime
pd.options.dispaly.float_format = '{:.0f}'.format


def process_song_fie(cur, filepath):
    """
    This fuctions loads JSON files into the song table

    Parameters:
        ** args
            cur - the cursor connection to the database
            filepath - the filepath to the JSON song files
    
    Returns
        The data from the json files are loaded into the songs table 
    
    """
    #open song file
    data = pd.read_json(filepath, lines= True)
    song_df = pd.DataFrame(data)

    #transform the song_df to the needed table ie (song_table)
    song_data = song_df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    song_data.values.tolist()
    
    #insert data into the songs tables
    try:
        for row in song_data:
            cur.execute(song_table_insert, row)
    
    except psycopg2.Error as e:
        print("Error: Could not Insert into song table")
        print(e)

    #transform the song_df to the needed table ie (artist_table)
    artist_data = song_df[['artist_id', 'artist_name', 'artist_location', 'artists_latitude', 'artist_longitude']]
    artist_data.values.tolist()

      #insert data into the artist tables
    try:
        for row in artist_data:
            cur.execute(artist_table_insert, row)
    
    except psycopg2.Error as e:
        print("Error: Could not Insert into artist table")
        print(e)

def process_log_file(cur, filepath):
    """
    The function loads JSON log files into the tables: time, users and 
    songplays

    parameters:
        *args
            cur  - The cursor of connection to the database
            filepath - the filepath of the JSON log file
    
    processing steps:
        - entries from log file are filtered by the criteria page = 'Next Song'
        - timestamp data is broken down into:
            day, hour, month, week, year, weekday before insertion into the 
            dimension time table
        -   data realted to user are loaded inot the users table
        - data related to song plays are loaded into the songplays table
        artist_id and song _id are retrieved based on sql 'song_select'.
    
    Returns :
        the process data from the JSON file are laoded into the table

    """
    #open log file
    log_data = pd.read_json(filepath, lines=True)
    log_data_df = pd.DataFrame(log_data)

    # transform the log_data to form the time_table
    log_data_df = log_data_df[log_data["page"] == 'NextSong']
    log_data_df['datetime'] = pd.to_datetime(log_data_df['ts'], unit = 'ms')
    ts_df = log_data_df[['ts', 'datetime']].drop_duplicates()

    ts_df['timestamp'] = ts_df['datetime'].astype('int64')/1000000
    ts_df['hour'] = ts_df['datetime'].dt.hour
    ts_df['day'] = ts_df['datetime'].dt.day
    ts_df['week'] = ts_df['datetime'].dt.isocalendar().week
    ts_df['month'] = ts_df['datetime'].dt.month
    ts_df['year'] = ts_df['datetime'].dt.month
    ts_df['weekday'] = ts_df['datetime'].dt.weekday

    ts_df = ts_df[['timestap', 'hour', 'day', 'week', 'month', 'year', 'weekday']]
    
    time_data = ts_df[['timestap', 'hour','day', 'week', 'month', 'year', 'weekday']]
    time_data = np.array(time_data)
    time_data = time_data.transpose()
    time_data = time_data.astype('int64')

    column_labels = ['start_time', 'hour', 'day', 'week','month', 'year', 'weekday']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    try:
        for i, row in time_df.itterrows():
            cur.execute(time_table_insert, list(row))
    except psycopg2.Error as e:
        print("Error: Could not insert data to time table ")
        print(e)
    

    #transform the user table
    user_df = log_data_df[['userId', 'firstName', 'firstName', 'gender', 'level']]
    
    #insert data into 
    try:
        for i,row in user_df.iterrows():
            cur.execute(user_table_insert, list(row))
    except psycopg2.Error as e:
        print("Error: Could not insert data into user table") 
        print(e)
    
    songplay_df = log_data_df[['ts', 'userId', 'level', 'sessionId','location', 'userAgent','song', 'artist', 'length']]

    try:
        for index, row in songplay_df.itterrows():
            cur.execute(song_select, (row.song, row.artist, row.length))
            results = cur.fecthone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
        
        #insert songplay record
        songplay_data = [row.ts, row.userId, row.level, songid, artistid, row.sessionid, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)
    except psycopg2.Error as e:
        print("Error: Could not insert data into the songplay tavle")


def process_data(cur, conn,filepath, func):
    """
    The functions gets all the JSON from filepath and calls a function set in parameter
    to load data into database

    Params
        args*
            -cur - Get cursort to the database
            - conn - Creates connection to database.
            - func - the functions that loads JSON files into the database
    
    Returns:
        - The functions iterates over each JSON file foung
        - It calls the function set in arguement to load the data into tables

    """
    #get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*json"))
        for f in files:
            all_files.appenf(os.path.abspath(f))
    
    #get the number of files found
    num_files = len(all_files)
    print("{} files found in {}".format(num_files, filepath))

    # iterate over files and proces
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed'.format(i, num_files))
    
def main(): 
    """
    The main function connects to the database and calls other functions
    in the module to load JSON files into the database.
        
     """
    conn = psycopg2.connect("host= localhost user = postgres password = 9507024922 dbname = sparkifydb")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_fie)
    process_data(cur, conn, filepath='data/log_data', func = process_log_file)

    conn.close()

if __name__ == "__main__":
    main()