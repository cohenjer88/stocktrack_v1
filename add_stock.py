"""This script adds a stock to the db

Syntax:

$ python add_stock.py [symbol_name_1] [symbol_name_2] ... [symbol_name_n] [start_date]

where [start_date] takes the form of yyyy-mm-dd


"""

import sys
from alpha_vantage.timeseries import TimeSeries
import sqlite3
import pandas as pd 

conn = sqlite3.connect('stocktracker.db')
c = conn.cursor()

print("\n")
print("**************************************************************************")
print("**************************************************************************")
print("**************************************************************************")
print("\n")
print("Welcome to the Stocktracker 3000 Add Tool!")
print("\n")

if len(sys.argv) < 3:
    print("ERROR: Please give at least one symbol name and a start date")
    sys.exit()
elif len(sys.argv) == 3:
	print("Adding one company to the stock tracking database")
else:
	print("Adding {} companies to the stock tracking database".format(len(sys.argv)-2))

## comment: api credentials

api_key = '29189WGEJUA4P5X6'

## comment: MySQL credentials

conn = sqlite3.connect('stocktracker.db')
c = conn.cursor()

##the actual function to add lines from api to database


def add(stock_name, start_date):
    ts = TimeSeries(key=api_key, output_format='pandas', indexing_type='integer') #this is some rando's wrapper, eventually want to replace
    data = ts.get_daily(symbol=stock_name) #this is the api call
    df = data[0] #data returns a dataframe and metadata, dataframe is [0] and metadata is [1]
    df['stock_name'] = stock_name #create a column called stock_name that is a fixed value 
    close_price = df[['date', 'stock_name', '4. close']]
    close_price = close_price[(close_price['date'] >= start_date)]
    st_records = list(close_price.itertuples(index=False, name=None))
    sp_records = (stock_name, start_date, 'null')
    print("\n")
    print("Loading {} into the stock_tracker database at {}".format(stock_name, start_date))
    print("\n")
    c.executemany('INSERT INTO stock_tracker VALUES (?,?,?)', st_records)
    print("Loading of {} into stock_tracker complete".format(stock_name))
    print("\n")
    print("Loading {} into the stock_portfolio database at {}".format(stock_name, start_date))
    print("\n")
    c.execute('INSERT INTO stock_portfolio VALUES (?,?,?)', sp_records)
    print("Loading of {} into stock_portfolio complete".format(stock_name))
    print("\n")
    

##looping all arguments 

for i in range(1, len(sys.argv)-1): #ignore last element of sys.argv, as it's a date 
    named_stock = sys.argv[i]
    named_start_date = sys.argv[len(sys.argv)-1]
    c.execute('SELECT * from stock_portfolio where stock_name = "{}"'.format(named_stock)) #tricky, you have to remember the second pair of quotes
    test = c.fetchone()
    if not test: #if the select statement returns nothing 
        try:
            add(named_stock, named_start_date)
        except KeyError as ke:
            print("You got some weird shit in your statement")
            raise
    else:
        print("\n")
        print("{} has already been added! Moving on to the next stock ... ".format(named_stock))
        
print("\n")    
print("All additions complete! I love you, balalala! Mwaaaaaah!")
print("\n")
print("**************************************************************************")
print("**************************************************************************")
print("**************************************************************************")
print("\n")

conn.commit()

conn.close()


"""
Notes: len(sys.argv) gives # of arguments + script name 
"""