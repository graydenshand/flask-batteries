#!/opt/homebrew/bin/python3
import os
import sys
import shutil

name = sys.argv[1]

print("Destroying app named: %s" % name)

shutil.rmtree(name)