import sqlite3
from sqlite3 import Error

def create_connection(db_file):
	"""create a database connection to a SQLite database """
	try: 
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
	except Error as e:
		print(e)
	finally:
		conn.close()

if __name__ == '__main__':
	create_connection("/home/dunhof/Documents/stocktrack_v1/stocktracker.db")

print("Database created at: /home/dunhof/Documents/stocktrack_v1/stocktracker.db")

print("...") 

print("Now creating tables")

print("...")

conn = sqlite3.connect('stocktracker.db')

c = conn.cursor()

c.execute('''CREATE TABLE stock_tracker 
             (close_date datetime, stock_name varchar(20), price real)''')

print("Stock_tracker table created")

print("...")

c.execute('''CREATE TABLE stock_portfolio
			 (stock_name varchar(20), start_date datetime, end_date datetime)''')

print("Stock_portfolio table created")

print("...")

print("DB and necessary tables complete. Time to get your tracking on!")

