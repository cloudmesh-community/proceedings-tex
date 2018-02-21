import glob
import subprocess
import textwrap
import re

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
        if '@Comment' in line :
            pass
        elif '@' in line :
            found.append(line.split("{")[1].split(",")[0])
    return found
    
    
print('\part{Technologioes}')

print('\chapter{New Technologies}')

for d in abstracts:
    if " " in d:
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
        output2 = subprocess.check_output(["chktex", latex])
        output2_str = textwrap.fill(output2.decode("utf-8"), 80)      
        print('\\begin{tiny}')
        print('\\begin{verbatim}')
        if output1_str is not '':
            print("lacheck:")
            print (output1_str)
        if output2_str is not '':
            print("chktex:")
            print (output2_str)
        print('\\end{verbatim}')
        print('\\end{tiny}')    

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
    issue=url + '/issue'

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
    
        
    print('')        
    print('\\end{IU}')
         
    
# https://github.com/cloudmesh-community/hid-sp18-521/blob/master/technology/abstract-athena.tex
