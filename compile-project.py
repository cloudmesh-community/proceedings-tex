#!/usr/bin/env python
import glob
import subprocess
import textwrap
import re
import sys
import os
import yaml
import textwrap
from pprint import pprint

s = {}

def compile_papers():
    papers = sorted(glob.glob('../hid-sp*/project-paper/content.tex'))

    for paper in papers:
        print (79* "%")
        print ("% BEGIN", paper)
        print (79 * "%")
        d = os.path.dirname(paper)
        command = "cd {d}; make".format(d=d)
        status = os.system(command)
        s[paper] = status
        print (79* "%")
        print ("% END", paper)
        print (79 * "%")

    
compile_papers()
pprint(s)
