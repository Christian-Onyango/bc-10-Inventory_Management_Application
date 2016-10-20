#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    inventoryapp item_add <name> <total_amount_available> <cost_per_item> <date_added> <status> <description>...
    inventoryapp item_remove <item_id>
    inventoryapp item_list
    inventoryapp item_export <file_name>
    inventoryapp item_checkout <item_id>
    inventoryapp item_checkin <item_id>
    inventoryapp item_view <item_id>
    inventoryapp item_search <search_query>
    inventoryapp assetvalue
    inventoryapp (-i | --interactive)
    inventoryapp (-h | --help)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
import sqlite3
import time
import datetime
import csv

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg,):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive (cmd.Cmd):

    intro = print("Hello, welcome to my inventory management application")
    print ('''
    [options]
    item_add:   Adds an item to the inventory
    item_remove: Removes an item from the inventory
    item_list:  Lists all the items available in the inventory with their status (checked out or checked in)
    item_export: Exports inventory data as a CSV file
    item_checkout : Checkout an item from the warehouse/store
    item_checkin : Checkin an item that was previously checked out
    item_view : View all the item details for item with id and shows a log of all the times this item was checked out and checked in 
    item_search: Return a list of all the items that match the search_query
    compute_assetvalue: Calculate total assets value
    quit Exists the system''')

    prompt = '(inventoryapp) '
    file = None


    def __init__(self):
        super(MyInteractive, self).__init__()
        # or cmd.Cmd.__init__(self)

        conn = sqlite3.connect('inventorystore.db')
        c = conn.cursor()
        print('''opened database successfully''')
        c.execute('CREATE TABLE IF NOT EXISTS InventoryManagement(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, total_amount_available INTEGER, cost_per_item REAL, date_added TEXT, status INTEGER, description TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS InventoryLog(id INTEGER PRIMARY KEY AUTOINCREMENT, item_id INTEGER, date_added TEXT, event TEXT)')

        conn.commit()
        c.close()
        conn.close()


    @docopt_cmd
    def do_item_add(self, args,):
        """Usage: item_add <name> <total_amount_available> <cost_per_item> <date_added> <status> <description>..."""
        description = args['<description>']
        args['<description>'] = " ".join(description)
        
        print("Books")
        print(args)

        name = args['<name>']
        total_amount_available = args['<total_amount_available>']
        cost_per_item = args['<cost_per_item>']
        date_added = args['<date_added>']
        status = args['<status>']
        description = args['<description>']
        unix = time.time()
        date_added = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))
        status_ = 0
        if status == 'TRUE':
            status_ = 1
        else:
            status_ = 0


        conn = sqlite3.connect('inventorystore.db')
        c = conn.cursor()
        c.execute("INSERT INTO InventoryManagement(name, total_amount_available, cost_per_item, date_added, status, description) VALUES(?, ?, ?, ?, ?, ?)",(name, total_amount_available, cost_per_item, date_added, status_, description))
        conn.commit()
        c.close()
        conn.close()
 

    @docopt_cmd
    def do_item_remove(self, args):
        """Usage: item_remove <item_id>"""
        print("Remove")
        print(args)

        item_id = args['<item_id>']

        conn = sqlite3.connect('inventorystore.db')
        c = conn.cursor()
        c.execute("DELETE FROM InventoryManagement WHERE id = " + item_id)
        if conn.total_changes == 0:
            print("Item_id not found")
        else:
            print("Removed item_id: " + item_id)

        conn.commit()
        c.close()
        conn.close()
        # inventoryupdated.list(args)


    @docopt_cmd
    def do_item_list(self, args):
        """Usage: item_list"""
        conn = sqlite3.connect('inventorystore.db')
        c = conn.cursor()
        c.execute("SELECT id, name, total_amount_available,cost_per_item,date_added,CASE WHEN status = 1 THEN 'checked in' ELSE 'checked out' END AS status,description FROM InventoryManagement")
        print(c.fetchall())
        conn.commit()
        c.close()
        conn.close()

    @docopt_cmd
    def do_item_export(self, args):
        """Usage: item_export <file_name>"""
        print("Export")
        print(args)

        file_name = args['<file_name>']

        conn = sqlite3.connect('inventorystore.db')
        c = conn.cursor()
        data = c.execute("SELECT id, name, total_amount_available,cost_per_item,date_added,CASE WHEN status = 1 THEN 'checked in' ELSE 'checked out' END AS status,description FROM InventoryManagement")
        with open(file_name +'.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'total_amount_available', 'cost_per_item', 'date_added', 'status', 'description'])
            writer.writerows(data)
        conn.commit()
        c.close()
        conn.close()

    @docopt_cmd
    def do_item_checkout(self, args):
        """Usage: item_checkout <item_id>"""
        print("checkout")
        print(args)

        item_id = args['<item_id>']

        unix = time.time()
        date_added = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))

        conn = sqlite3.connect('inventorystore.db')
        c = conn.cursor()
        c.execute("UPDATE InventoryManagement SET status = 0 WHERE id = " + item_id)
        if c.rowcount == 0:
            print("Item already checked out")
        else:
            c.execute("INSERT INTO InventoryLog (item_id, date_added, event) VALUES (?, ?, ?)", (item_id, date_added, 'checked out'))
            print("Item checked out")
        conn.commit()
        c.close()
        conn.close()

    @docopt_cmd
    def do_item_checkin(self, args):
        """Usage: item_checkin <item_id>"""
        print("checkin")
        print(args)

        item_id = args['<item_id>']
        unix = time.time()
        date_added = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))

        conn = sqlite3.connect('inventorystore.db')
        c = conn.cursor()
        c.execute("UPDATE InventoryManagement SET status = 1 WHERE id = " + item_id)
        if c.rowcount == 0:
            print("Item already checked in")
        else:
            c.execute("INSERT INTO InventoryLog (item_id, date_added, event) VALUES (?, ?, ?)", (item_id, date_added, 'checked in'))
            print("Item checked in")
        conn.commit()
        c.close()
        conn.close()

    @docopt_cmd
    def do_item_view(self, args):
        """Usage: item_view <item_id>"""
        print("itemview")
        print(args)

        item_id = args['<item_id>']

        conn = sqlite3.connect('inventorystore.db')
        c = conn.cursor()
        print("ITEM DETAILS")
        c.execute("SELECT id, name, total_amount_available,cost_per_item,date_added,CASE WHEN status = 1 THEN 'checked in' ELSE 'checked out' END AS status,description FROM InventoryManagement WHERE id =" + item_id)
        print(c.fetchall())
        print("LOGS")
        c.execute("SELECT date_added, event FROM InventoryLog WHERE item_id =" + item_id)
        print(c.fetchall())
        conn.commit()
        c.close()
        conn.close()

    @docopt_cmd
    def do_item_search(self, args):
        """Usage: item_search <search_query>"""
        print("Search")
        print(args)

        search_query = args['<search_query>']

        conn = sqlite3.connect('inventorystore.db')
        c = conn.cursor()
        c.execute("SELECT id, name, total_amount_available,cost_per_item,date_added,CASE WHEN status = 1 THEN 'checked in' ELSE 'checked out' END AS status,description FROM InventoryManagement WHERE name LIKE '%" + search_query + "%'")
        print(c.fetchall())
        conn.commit()
        c.close()
        conn.close()

    @docopt_cmd
    def do_assetvalue(self, args):
        """Usage: assetvalue"""

        conn = sqlite3.connect('inventorystore.db')
        c = conn.cursor()
        c.execute('select cost_per_item from InventoryManagement')
        rows = c.fetchall()
        asset_val = 0
        for row in rows:
            # print row
            val = row[0]
            # print val
            asset_val += int(val)
        print ("Total asset value is: {} ".format(asset_val))



    def do_quit(self, args):
        """Quits out of Interactive Mode."""
        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)