import sys
import sqlite3
import pandas as pd 

conn = sqlite3.connect('stocktracker.db')
c = conn.cursor()

print("\n")
print("**************************************************************************")
print("**************************************************************************")
print("**************************************************************************")
print("\n")
print("Welcome to the Stocktracker 3000 Drop Tool!")
print("\n")

if len(sys.argv) < 2:
    print("ERROR: Please give at least one symbol name")
    sys.exit()
elif len(sys.argv) == 2:
	print("Dropping one company to the stock tracking database")
else:
	print("Dropping {} companies to the stock tracking database".format(len(sys.argv)-1))
	print("\n")

for i in range(1, len(sys.argv)):
	named_stock = sys.argv[i]
	c.execute('SELECT * from stock_portfolio where stock_name = "{}"'.format(named_stock))
	test = c.fetchone()
	if test:
		c.execute('DELETE from stock_tracker where stock_name = "{}"'.format(named_stock))
		print("Dropping {} from the stock_tracker table".format(named_stock))
		print("\n")
		c.execute('DELETE from stock_portfolio where stock_name ="{}"'.format(named_stock))
		print("Dropping {} from the stock_portfolio table".format(named_stock))
		print("\n")

print("Dropping is complete!")

print("\n")
print("**************************************************************************")
print("**************************************************************************")
print("**************************************************************************")
print("\n")

conn.commit()

conn.close()