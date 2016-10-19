#!/usr/bin/env python
"""
Usage:
    InventoryApp item_add <name> <description> <total_amount_available> <cost_per_item> <status>
    InventoryApp (-i)
Options:
    -i, --interactive  Interactive Mode 
    -h, --help Show this screen and exit
    -v,  --version Show version
"""
from docopt import docopt, DocoptExit
import cmd
from inventoryupdated import *
import os
import sys
#import click
#import userexp

#userexp.start()


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
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

# items = []
class Item(cmd.Cmd):
    # prompt = "InventoryApp>>> "
    print("Hello")
    prompt = '(InventoryApp) '
    file = None    

    @docopt_cmd
    def do_item_add(self, arg):
        """Usage: item_add <name> <description> <total_amount_available> <cost_per_item> <status>"""
        # name = arg["<name>"]
        # description = arg["<description>"]
        # total_amount_available = arg["<total_amount_available>"]
        # cost_per_item = arg["<cost_per_item>"]
        # status = arg["<status>"]

        # item_add(name, description, total_amount_available, cost_per_item, status)
        # print("\t" + "*"*42)
        # print (Back.GREEN + ("\t\t name\t\t description\t\t total_amount_available\t\t cost_per_item\t\t status\t\t "))
        # print("\t" + "*"*42)
        # print (Back.YELLOW + "\t\t{} \t\t{}".format(name, description, total_amount_available, cost_per_item, status))
        # print("\t" + "*"*42)
        pass

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    Item().cmdloop()

print(opt)