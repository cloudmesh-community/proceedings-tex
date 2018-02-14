.PHONY: book images

FILE=bio
#FLAGS=-interaction nonstopmode -halt-on-error -file-line-error
#FLAGS=-interaction nonstopmode  -file-line-error
FLAGS=-shell-escape
CLOUD=cloud
FLAGS=-shell-escape -output-directory=dest -aux-directory=dest


DEFAULT=$(CLOUD)

LATEX=pdflatex


all: dest biolist
	latexmk $(FLAGS) -pvc -view=pdf $(FILE)

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
	open abstract.pdf

