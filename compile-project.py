#!/usr/bin/env python
import glob
import subprocess
import textwrap
import re
import sys
import os
import yaml
import textwrap

def compile_papers():
    papers = sorted(glob.glob('../hid-sp*/project-paper/content.tex'))

    for paper in papers:
        print ("%")
        print ("%", paper)
        print ("%")
        d = os.path.dirname(paper)
        command = "cd {d}; make".format(d=d)
        os.system(command)

    
compile_papers()
