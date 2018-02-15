import glob

abstracts = sorted(glob.glob('../hid-sp*/technology/abstract-*.tex'))


print('\part{Technologioes}')

print('\chapter{New Technologies}')

for d in abstracts:
    print('\\input{{{file}}}'.format(file=d))
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
    print('\\end{IU}')
         
    
# https://github.com/cloudmesh-community/hid-sp18-521/blob/master/technology/abstract-athena.tex
