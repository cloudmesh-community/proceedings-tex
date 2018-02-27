import glob
import subprocess
import textwrap
import re
import sys

exclude = ['hid-sp18-514']

abstracts = sorted(glob.glob('../hid-sp*/technology/abstract-*.tex'))
 
def readfile(filename):
    file = open(filename, "r") 
    s = file.read() 
    file.close()
    return (s)


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

print('\part{Technologioes}')

print('\chapter{New Technologies}')

for d in abstracts:
    
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

    if "@" in  f or "author =" in f: 
        pass
    else:
        latex = d.replace(".tex","")

        print('\\input{{{file}}}'.format(file=latex))
        hid = d.split("/")[1]
        filename = d.split("/")[3]    

        
        print('')    
        print('\\begin{IU}')
        print('')
        print(hid)
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
        print ('Wordcount:', texcheck.wc(f) )        
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
                print("\n", 'Error Citation Label wrong:', l)
        if "howpublished = {Web}" in bib:
            print ('\nError: you did not use howpublished = \{Web Page\},')

    except Exception as e:
        print (hid + ".bib", "is missing")


    output2 = subprocess.check_output(["perl", "-ane", "'{ if(m/[[:^ascii:]]/) { print  } }'",  "*.tex", "*.bib"])
    output2 = output2.decode("utf-8")
        
    output2_str = textwrap.fill(output2, 80)    
    if output1_str is not '':
            print("non-ASCII:")
            print('\\begin{tiny}')            
            print('\\begin{verbatim}')
            print (output2_str)
            print('\\end{verbatim}')            
            print('\\end{tiny}')    


    print('')        
    print('\\end{IU}')
         
    
# https://github.com/cloudmesh-community/hid-sp18-521/blob/master/technology/abstract-athena.tex
