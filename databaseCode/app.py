#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    inventoryapp item_add <name> <description> <total_amount_available> <cost_per_item> <status>
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
import inventoryupdated


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


class MyInteractive (cmd.Cmd):

    prompt = '(inventoryapp) '
    file = None

    @docopt_cmd
    def do_item_add(self, args):
        """Usage: inventoryapp item_add <name> <description> <total_amount_available> <cost_per_item> <status>"""
        
        print("am here")
        print()

    @docopt_cmd
    def do_list_items(self, args):
        """Usage: inventoryapp list"""

        inventoryupdated.list(args)

    def do_quit(self, args):
        """Quits out of Interactive Mode."""
        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)