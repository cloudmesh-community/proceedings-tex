PHONY: all
all:   bio-list.tex

bio-list.tex: $(wildcard hid-sp*/bio-*.tex)
	ls hid-sp*/bio-*.tex | awk '{printf "\\input{%s}\n", $$1}' > bio-list.tex
