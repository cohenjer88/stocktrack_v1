from alpha_vantage.timeseries import TimeSeries
import sqlite3
import pandas as pd

# api piece

ts = TimeSeries(key='29189WGEJUA4P5X6', output_format='pandas', indexing_type='integer')

data = ts.get_daily(symbol='GOOGL')

df = data[0] # data arrives in a tuple with two elements, first element a df and second metadata

close_price = df[['date', '4. close']]

records = list(close_price.itertuples(index=False, name=None))

# database piece

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute('''CREATE TABLE stock_tracker 
             (close_date datetime, price real)''')

c.executemany('INSERT INTO stock_tracker VALUES (?,?)', records)

for row in c.execute('SELECT * FROM stock_tracker where close_date > "2018-11-01" order by close_date'):
	print(row)

conn.close()

