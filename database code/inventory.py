import sqlite3
import time
import datetime

conn = sqlite3.connect('Inventory.db')
c = conn.cursor()
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS InventoryManagement(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, total_amount_available INTEGER, cost_per_item REAL, date_added TEXT, status INTEGER)')

def add(name, description, total_amount_available, cost_per_item, status):
    date_added = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))

    c.execute("INSERT INTO InventoryManagement(name, description, total_amount_available, cost_per_item, date_added, status) VALUES(?, ?, ?, ?, ?, ?)",(name, description, total_amount_available, cost_per_item, date_added, status))
    conn.commit()
    c.close()
    conn.close()
