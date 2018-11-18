"""This script adds a stock to the db

Syntax:

$ python add_stock.py [symbol_name_1] [symbol_name_2] ... [symbol_name_n] [start_date]


"""

import sys
from alpha_vantage.timeseries import TimeSeries
import sqlite3
import pandas as pd 


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
c.execute('''CREATE TABLE stock_tracker 
             (close_date datetime, stock_name varchar(20), price real)''')

##the actual function to add lines from api to database


def add(stock_name, start_date):
    ts = TimeSeries(key=api_key, output_format='pandas', indexing_type='integer')
    data = ts.get_daily(symbol=stock_name)
    df = data[0]
    df['stock_name'] = stock_name
    close_price = df[['date', 'stock_name', '4. close']]
    close_price = close_price[(close_price['date'] >= start_date)]
    records = list(close_price.itertuples(index=False, name=None))
    print("Loading {} into the stock_tracker database at {}".format(stock_name, start_date))
    print("...")
    c.executemany('INSERT INTO stock_tracker VALUES (?,?,?)', records)
    print("Loading of {} complete".format(stock_name))
    print("...")
    


##looping all arguments 

for i in range(1, len(sys.argv)):
	try:
		add(sys.argv[i], sys.argv[len(sys.argv)-1])
	except KeyError:
		pass

print("All additions complete! I love you, balalala! Mwaaaaaah!")

conn.commit()

conn.close()


"""
Notes: len(sys.argv) gives # of arguments + script name 
"""