all: latexmk

latexmk:
	latexmk -pdf -f ML_Method_Report_Template

todo:
	grep -R -s -n todo *.tex

clean:
	rm -f *.fls *.fdb_latexmk *.aux *.log *.dvi *.pdf *.bbl *.blg *.ilg *.ind *.toc *.idx *.out *.nav *.snm
