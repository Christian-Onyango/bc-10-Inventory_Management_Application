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

    def __init__(self):
        conn = sqlite3.connect('willys.db')
        c = conn.cursor()
        print('opened database successfully')
        c.execute('CREATE TABLE IF NOT EXISTS InventoryManagement(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, total_amount_available INTEGER, cost_per_item REAL, date_added TEXT, status INTEGER, description TEXT)')
        print('created table InventoryManagement')

    intro = print("Hello, welcome to my inventory management application")
    print ('''
    [options]
    item_add:   Adds an item to the inventory
    item_remove: Removes an item from the inventory
    item_list:  Lists all the items available in the inventory with their status (checked out or checked in)
    list_export_csv: Exports inventory data as a CSV file
    item_checkout : Checkout an item from the warehouse/store
    item_checkin : Checkin an item that was previously checked out
    item_view : View all the item details for item with id and shows a log of all the times this item was checked out and checked in 
    item_search: Return a list of all the items that match the search_query
    compute_assetvalue: Calculate total assets value
    quit Exists the system''')

    prompt = '(inventoryapp) '
    file = None

    @docopt_cmd
    def do_item_add(self, args,):
        """Usage: item_add <name> <total_amount_available> <cost_per_item> <date_added> <status> <description>..."""
        description = args['<description>']
        args['<description>'] = " ".join(description)
        
        print("Books")
        print(args)

    @docopt_cmd
    def do_remove_item(self, args):
        """Usage: inventoryapp list"""

        # inventoryupdated.list(args)
        pass

    def do_quit(self, args):
        """Quits out of Interactive Mode."""
        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)