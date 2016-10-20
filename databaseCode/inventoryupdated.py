import sqlite3
import time
import datetime
import sys

conn = sqlite3.connect('Inventory.db')
c = conn.cursor()
def create_table():
    print("creating table")
    c.execute('CREATE TABLE IF NOT EXISTS InventoryManagement(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, total_amount_available INTEGER, cost_per_item REAL, date_added TEXT, status INTEGER, description TEXT)')

def add(args):
    print("inside add")
    name = args['<name>']
    total_amount_available = args['<total_amount_available>']
    cost_per_item = args['<cost_per_item>']
    date_added = args['<date_added>']
    status = args['<status>']
    description = args['<description>']
    unix = time.time()
    date_added = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))

    c.execute("INSERT INTO InventoryManagement(name, total_amount_available, cost_per_item, date_added, status, description) VALUES(?, ?, ?, ?, ?, ?)",(name, total_amount_available, cost_per_item, date_added, status, description))
    c.commit()
    c.close()
    

def remove(item_id):
    c.execute("DELETE FROM InventoryManagement WHERE id = " + item_id)
    c.commit()
def list():
    c.execute("SELECT * FROM InventoryManagement")
    print(c.fetchall())

def export(file_name):
    data = c.execute("SELECT * FROM InventoryManagement")
    with open(file_name +'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'total_amount_available', 'cost_per_item', 'date_added', 'status', 'description'])
        writer.writerows(data)

def checkout(item_id):
    c.execute("UPDATE InventoryManagement SET status = 0 WHERE id = " + item_id)
    conn.commit()

def checkin(item_id):
    c.execute("UPDATE InventoryManagement SET status = 1 WHERE id = " + item_id)
    conn.commit()
def view(item_id):
    c.execute("SELECT * FROM InventoryManagement WHERE id = " + item_id)
    print(c.fetchall())

def search(search_query):
    c.execute(search_query)
    return c.fetchall()
def assetvalue():
    c.execute("SELECT sum(cost_per_item * total_amount_available)")
    print(c.fetchall())

create_table()




    
