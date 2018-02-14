biolist: $(wildcard ../hid-sp*/bio-*.tex)
	ls ../hid-sp*/bio-*.tex | awk '{printf "\\input{%s}\n", $$1}' > bio-list.tex
	cat bio-list.tex


check:
	grep "&" ../hid-sp18-*/bio-*.tex 
	grep '\$$' ../hid-sp18-*/bio-*.tex 
	grep "_" ../hid-sp18-*/bio-*.tex


clean:
	rm -f	*.pdf *.bbl *.log *.blg *.aux *.out *.idx *.run.xml *.bcf
