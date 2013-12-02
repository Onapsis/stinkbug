import sys
import argparse
import os

parser = argparse.ArgumentParser(description='Stinkbug',add_help=False) 

# add a subparser for the modules
subparsers = parser.add_subparsers(help="modules")

for f in os.listdir("./lib/modules"):
    # add each of the modules subcommands
    if not (".pyc" in f or "__init__" in f):
        package = "lib.modules"
        name = f.replace(".py","")
        imported = getattr(__import__(package, fromlist=[name]), name)
        imported.load_(subparsers)

args = parser.parse_args()
args.func(args)

