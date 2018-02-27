.PHONY: book images

FILE=vonLaszewski-cloud-vol-7
#FLAGS=-interaction nonstopmode -halt-on-error -file-line-error
#FLAGS=-interaction nonstopmode  -file-line-error
FLAGS=-shell-escape
CLOUD=cloud
FLAGS=-shell-escape -output-directory=dest -aux-directory=dest


DEFAULT=$(CLOUD)

LATEX=pdflatex


all: clean dest biolist
	latexmk -jobname=$(FILE) $(FLAGS) -pvc -view=pdf $(FILE) 

pdflatex: clean dest biolist
	pdflatex $(FILE)

biolist: $(wildcard ../hid-sp*/bio-*.tex)
	python bios.py >  bio-list.tex

#ls ../hid-sp*/bio-*.tex | awk '{printf "\\input{%s}\n", $$1}' > bio-list.tex
#	cat bio-list.tex


check:
	grep "&" ../hid-sp18-*/bio-*.tex 
	grep '\$$' ../hid-sp18-*/bio-*.tex 
	grep "_" ../hid-sp18-*/bio-*.tex


clean:
	rm -f	*.pdf *.bbl *.log *.blg *.aux *.out *.idx *.run.xml *.bcf
	rm -rf dest

dest:
	mkdir dest

view:
	open dest/$(FILE).pdf

google:
	gdrive update 1h6_ZRmlCRIFMHG861wSyriPzn9rXxgKT dest/$(FILE).pdf

publish: google
	echo done

pull:
	cd ..; cms community pull
