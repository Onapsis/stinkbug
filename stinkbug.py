import sys
import argparse
import os

# The required arguments for authentication
parser = argparse.ArgumentParser(description='Stinkbug',add_help=False) 

# load the subcommands specific to this module
subparsers = parser.add_subparsers(help="subparsers")

for f in os.listdir("./lib/modules"):
    if not (".pyc" in f or "__init__" in f):
        package = "lib.modules"
        name = f.replace(".py","")
        imported = getattr(__import__(package, fromlist=[name]), name)
        imported.load_(subparsers)

args = parser.parse_args()
args.func(args)

