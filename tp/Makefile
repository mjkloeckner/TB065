DOCNAME=main

all: main

.PHONY: clean

main:
	pdflatex $(DOCNAME).tex
	bibtex $(DOCNAME)
	pdflatex $(DOCNAME).tex
	pdflatex $(DOCNAME).tex

open: main
	nohup zathura $(DOCNAME).pdf > /dev/null 2>&1 &

clean:
	rm -ff *.blg *.bbl *.aux *.lof *.out *.log
