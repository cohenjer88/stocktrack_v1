import quandl
import sqlite3

# api piece

quandl.ApiConfig.api_key = 'qAzpRpsh2yD1UcL4fEQq'

ingestion = quandl.get('EOD/AAPL', column_index='4', 
						start_date = '2018-10-15', end_date = '2018-10-19')

ingestion.reset_index(inplace=True)

ingestion['Date'] = ingestion['Date'].dt.date

print(ingestion)

records = list(ingestion.itertuples(index=False, name=None))

print(records)

# database piece

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute('''CREATE TABLE stock_tracker 
             (date text, price real)''')

c.executemany('INSERT INTO stock_tracker VALUES (?,?)', records)

for row in c.execute('SELECT * FROM stock_tracker order by date'):
	print(row)

conn.close()

