#!/usr/bin/env python
import glob
import subprocess
import textwrap
import re
import sys
import os

exclude = ['hid-sp18-514']

abstracts = sorted(glob.glob('../hid-sp*/technology/abstract-*.tex'))
bibs = sorted(glob.glob('../hid-sp*/technology/hid-*.bib'))

with open("vol7-bib.tex", "w") as f:
    print("\\addbibresource{hid-sample.bib}", file=f)  
    for b in bibs:
        print("\\addbibresource{{{bib}}}".format(bib=b), file=f)

def readfile(filename):
    file = open(filename, "r") 
    s = file.read() 
    file.close()
    return str(s)


def find_labels(content):
    found = []
    lines = content.split("\n")
    for line in lines:
        if '@Comment' in line or '@comment' in line :
            pass
        elif '@' in line :
            found.append(line.split("{")[1].split(",")[0])
    return found

class texcheck(object):

    @staticmethod
    def filename(name):        
        if ' ' in name or '_' in name:
            return False
        return True
    
    def citation_label(name):
        tmp = name.strip()
        if ' ' in tmp or '_' in tmp:
            return False
        if not tmp.startswith('hid-'):
            return False
        return True

    def http_in_body(content):
        if "http://" in content or "https://" in content:
            return True
        return False

    def wc(content):
        words = content.split(' ')
        return len(words)



preface = readfile("preface-vol7.tex")
print(preface)

print("\\section{Missing hid prefix in label}")
os.system('grep -L "cite{hid" ../hid-sp18*/technology/abstract-*.tex > vol7-cite-error-a.tex')

print("\\begin{verbatim}")
cite_error_a = readfile("vol7-cite-error-a.tex")
print(cite_error_a)
print("\\end{verbatim}")

print("\\section{Missing citation}")
os.system('grep -L "cite{" ../hid-sp18*/technology/abstract-*.tex > vol7-cite-error-b.tex')

print("\\begin{verbatim}")
cite_error_b = readfile("vol7-cite-error-b.tex")
print(cite_error_b)
print("\\end{verbatim}")

#for d in abstracts:
#    print(d)
#    os.system("perl -ane ’{ if\(m/[[:^ascii:]]\) { print  } }’ > error-char.tex")
#    r = readfile("error-char.tex")
#    print (r)

#for d in bibs:
#    print(d)
#    os.system("perl -ane ’{ if\(m/[[:^ascii:]]\) { print  } }’ > error-char.tex")
#    r = readfile("error-char.tex")
#    print (r)

#sys.exit()

print('\part{Technologioes}')

print('\chapter{New Technologies}')

for d in abstracts:
    if d in cite_error_a or d in cite_error_b:
        continue


    if not texcheck.filename(d):
        print("\section{{{}}}".format(d))
        print ("Filename invalid")
        continue
    
    try:
        f = readfile(d)
    except Exception as e:
        print("\section{{{}}}".format(d))
        f = str(e)
        print (f)
        continue

    f = f.replace("``", "\color{blue}``\emph{")
    f = f.replace("''", "}''\color{black}")
                  
    if "@" in  f or "author =" in f: 
        pass
    else:
        latex = d.replace(".tex","")

        if "“" in f or '"' in f:
           print("ERROR: Illegal quotes in the file skipping inclusion. Please fix the folllowing file:")
        else:
            #print('\\input{{{file}}}'.format(file=latex))
            print (f)
            
        hid = d.split("/")[1]
        filename = d.split("/")[3]    

        
        
        print('')    
        print('\\begin{IU}')
        print('')
        print(hid)
        if "\\index{" not in f:
            print('')
            print("ERROR: index is missing")
        if "footnote" in f:
            print('')
            print("ERROR: entry contains a footnote that has not yet been addressed")
        #print('')    
        
        #print('')    

        #print(d)
        url = 'https://github.com/cloudmesh-community/{hid}/blob/master//technology/{filename}'.format(hid=hid, filename=filename)
        print('')    
        print('\\href{{{url}}}{{{filename}}}'.format(filename=filename, url=url))

        print('')
        output1 = subprocess.check_output(["lacheck", latex])
        output1_str = textwrap.fill(output1.decode("utf-8"), 80)      
        output2 = subprocess.check_output(["chktex", "-q", "-n", "13", "-n", "8", "-n", "29", latex])
        output2 = output2.decode("utf-8")
        output2 = output2.replace("ChkTeX v1.7.4 - Copyright 1995-96 Jens T. Berger Thielemann.", "")
        output2 = output2.replace("Compiled with POSIX extended regex support.", "")        
        


        
        output2_str = textwrap.fill(output2, 80)      

        print(' ')
        # not printing lacheck as it does not allow to exclude checks
        #if output1_str is not '':
        #    print("lacheck:")
        #    print('\\begin{tiny}')
        #    print('\\begin{verbatim}')
        #    print (output1_str)
        #    print('\\end{verbatim}')
        #    print('\\end{tiny}')    
        if output2_str is not '':
            print("chktex:")
            print('\\begin{tiny}')            
            print('\\begin{verbatim}')
            print (output2_str)
            print('\\end{verbatim}')            
            print('\\end{tiny}')    


        print ()
        count = texcheck.wc(f)
        print ('Wordcount:', count )
        if count < 130:
            print('')
            print ("WARNING: Short Abstract: Is there enough information for a reader to understand what it is?")
        print ()
        
        if texcheck.http_in_body(f):
            print("Error: URL found, use citation instead")

        #print (f)
        #print ("gregor")
        
        print('\\end{IU}')
        print('')
    

print('\part{Biographies}')

print('\chapter{Volume Contributors}')    



dirs = sorted(glob.glob('../hid-sp*/bio-*.tex'))

for d in dirs:
    print('\\input{{{file}}}'.format(file=d))
    hid = d.split("/")[1]

    print('')    
    print('\\begin{IU}')
    print('')
    print(hid)
    
    url = 'https://github.com/cloudmesh-community/'+ hid
    issue=url + '/issues'

    print('')
    print('\\url{{{url}}}'.format(url=url))
    
    print('')
    print('\\url{{{issue}}}'.format(issue=issue))

    # find abstracts
    location = '../{hid}/technology/abstract-*.tex'.format(hid=hid)
    abstracts = glob.glob(location)
    for a in abstracts:
        link = a.replace("../{hid}".format(hid=hid),"")
        url_a = "https://github.com/cloudmesh-community/{hid}/blob/master/{link}".format(link=link, hid=hid)
        filename = link.replace('/technology/', "")
        print ('')
        print ("\\href{{{url}}}{{{filename}}}".format(url=url_a, filename=filename))

    print('')            
    try:
        filename = "../{hid}/technology/{hid}.bib".format(hid=hid)
        bib = readfile(filename)
        url = 'https://github.com/cloudmesh-community/{hid}/blob/master//technology/{hid}.bib'.format(hid=hid, filename=filename)

        print('\\href{{{url}}}{{{filename}}}'.format(filename=filename, url=url))

        labels = find_labels(bib)
        for l in labels:
            if not l.startswith('hid'):
                print("\n", 'ERROR: Citation Label wrong: \\verb|', l,'|')
            if " " in l.strip():
                print("\n", 'ERROR: No spaces allowed in citation lables: \\verb|', l,'|')                
            if "_" in l.strip():
                print("\n", 'ERROR: No underscore allowed in citation lables: \\verb|', l,'|')                
        if "howpublished = {Web}" in bib:
            print ('\nError: you did not use howpublished = \{Web Page\},')

    except Exception as e:
        print (hid + ".bib", "is missing")


    #output2 = subprocess.check_output(["perl", "-ane", "'{ if(m/[[:^ascii:]]/) { print  } }'",  "*.tex", "*.bib"])
    #output2 = output2.decode("utf-8")
    
    #output2_str = textwrap.fill(output2, 80)    
    #if output2_str is not '':
    #        print("non-ASCII:")
    #        print('\\begin{tiny}')            
    #        print('\\begin{verbatim}')
    #        print (output2_str)
    #        print('\\end{verbatim}')            
    #        print('\\end{tiny}')    

    issues="../{hid}/github-issues.tex".format(hid=hid)
    if os.path.exists(issues):

        print('')            
        print ("\\input{{{issues}}}".format(issues=issues)) 

     
    print('')        
    print('\\end{IU}')
         
    
# https://github.com/cloudmesh-community/hid-sp18-521/blob/master/technology/abstract-athena.tex
