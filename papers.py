#!/usr/bin/env python
import glob
import subprocess
import textwrap
import re
import sys
import os
import yaml
import textwrap

def read_file(filename):
    with open(filename) as f:
        s = f.read()
        return (s)

def cat(filename):
    content = read_file(filename)
    print (content)
    
def compile_papers():
    papers = sorted(glob.glob('../hid-sp*/paper/content.tex'))

    for paper in papers:
        d = os.path.dirname(paper)
        command = "cd {d}; make".format(d=d)
        os.system(command)

def collect_list():
    authors = []
    papers = sorted(glob.glob('../hid-sp*/paper/content.tex'))
    for paper in papers:
        d = os.path.dirname(paper)
        d = os.path.dirname(d)        
        try:
            readme = read_file(d + "/README.yml")
            content = yaml.load(readme)
            authors.append(content['owner'])
        except Exception as e:
            print("% ERROR:", d, "README.md")
            print ("%", e)
    return authors

def print_list(authors):

    print(textwrap.dedent("""
    \chapter{List of Papers}

    \\begin{footnotesize}
    \\begin{longtable}{|rlllr|}
    \\hline 
    \\textbf{HID} & \\textbf{Author} & \\textbf{Title}  & \\textbf{Chapter} & \\textbf{Status} \\\\ 
    \\hline 
    \\hline"""))
    for author in authors:
        try:
            author['filename'] = "../{hid}/paper/content.tex".format(hid=author['hid'])
            content = read_file(author['filename'])
        except:
            content = "Error: file not found"
        try:
            author['status'] = re.findall("% status:\{(.*)\}", content)[0]
        except:
            author['status'] = "0"
        try:
            author['chapter'] = re.findall("% chapter:\{(.*)\}", content)[0]
        except:
            author['chapter'] = "undefined"

        try:
            author['title'] = re.findall("title\{(.*)\}", content)[0]
        except:
            author['title'] = "ERROR: Title not Found"
        try:
            print("{hid} & {lastname}, {firstname} & {title} & {chapter} & {status}\\\\".format(**author))
            print("\\hline")
        except:
            pass

    
    print("\\hline")
    print(textwrap.dedent("""
    \\end{longtable}
    \\end{footnotesize}
    \\newpage""").strip())
    
def collect_papers():
    pass
        
# compile_papers()
#sys.exit()

collect_papers()
authors = collect_list()


cat('start.tex')

print_list(authors)

for chapter in authors:

    try:
        chapter['filename'] = "../{hid}/paper/content.tex".format(**chapter)
        chapter['pdf'] = "../{hid}/paper/report.pdf".format(**chapter)
        content = read_file(chapter['filename'])
    except:
        chapter['filename'] = "Error: file not found"
        chapter['pdf'] = "Error: file not found"
        content = "Error: file not found"
        continue
        
    try:
        chapter['title'] = re.findall("title\{(.*)\}", content)[0]
    except:
        chapter['title'] = "ERROR: Title not Found"
    try:
        a = ' and '.join(re.findall("author\{(.*)\}", content))
        chapter['author'] = a
    except:
        chapter['author'] = "ERROR: Author not Found"
    try:
        chapter['keywords'] = re.findall("keywords\{(.*)\}", content)[0]
    except:
        chapter['keywords'] = "ERROR: Keywords not Found"

    print("\\phantomsection")

    print("\\addtocounter{chapter}{1}")
    print("\\addcontentsline{toc}{chapter}{\\arabic{chapter} ",
          chapter['hid'], '\\hfill',
              # 'Status:', d["status"],
              "\\newline",
          # d["chapter"], "\\newline",
          chapter["title"], "\\newline",
          chapter["author"], "}")
    if os.path.exists(chapter['pdf']):
        print ("\\includepdf[pages=-,pagecommand=\\thispagestyle{plain}]{" + chapter['pdf'] + "}")
    else:
        print ("%", chapter['pdf'], " not found")
        #if os.path.exists(tmplog):
        #    print ("\\VerbatimInput{" + tmplog + "}")
    #if with_log:
    #    if os.path.exists(log):
    #        print ("\\VerbatimInput{" + log + "}")
    #    else:
    #        print ("%", log, " not found")

cat('end.tex')
