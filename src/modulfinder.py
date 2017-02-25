#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from modulefinder import ModuleFinder
f = ModuleFinder()

# Run the main script
f.run_script('apparat.py')

# Get names of all the imported modules
names = list(f.modules.keys())

# Get a sorted list of the root modules imported 
basemods = sorted(set([name.split('.')[0] for name in names]))
# Print it nicely
print "\n".join(basemods)
