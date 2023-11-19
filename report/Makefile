all: latexmk

latexmk:
	latexmk -pdf -f ML_Method_Report_Template
	latexmk -pdf -f main 

todo:
	grep -R -s -n todo *.tex

clean:
	rm -f *.fls *.fdb_latexmk *.aux *.log *.dvi *.bbl *.blg *.ilg *.ind *.toc *.idx *.out *.nav *.snm *.thm
