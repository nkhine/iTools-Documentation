# Version
GIT_VERSION = $(shell bin/release.py)
DATE = $(shell date '+%F')

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python sphinx-link.py

# Internal variables.
PAPEROPT     = -D latex_paper_size=a4
ALLSPHINXOPTS   = -d .build/doctrees $(PAPEROPT) $(SPHINXOPTS) .

# Epydoc
ITOOLS_PATH= ${shell python -c "import itools; print itools.__path__[0]"}
EPYDOC=epydoc --no-frames --no-private --introspect-only --no-sourcecode --name itools --url http://www.hforge.org/itools/

.PHONY: clean help html pdf pickle htmlhelp latex changes linkcheck web

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  pdf       to make a standalone PDF file"
	@echo "  pickle    to make pickle files"
	@echo "  json      to make JSON files"
	@echo "  htmlhelp  to make HTML files and a HTML help project"
	@echo "  changes   to make an overview over all changed/added/deprecated items"
	@echo "  linkcheck to check all external links for integrity"
	@echo "  release   to make four tar.gz files to easily deploy the doc"

clean:
	-rm -rf .build/*
	-rm -f hforge-docs-*.tgz itools-examples-*.tgz itools-reference-*.tgz
	cd itools && make clean
	cd ikaaro && make clean
	cd git && make clean
	cd i18n && make clean
	cd itools-api && make clean

png-figures:
	cd itools && make png
	cd ikaaro && make png
	cd git && make png
	cd i18n && make png

pdf-figures:
	cd itools && make pdf
	cd ikaaro && make pdf
	cd git && make pdf
	cd i18n && make pdf

html: png-figures
	mkdir -p .build/html .build/doctrees
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) .build/html
	@echo
	@echo "Build finished. The HTML pages are in .build/html."

pickle:
	mkdir -p .build/pickle .build/doctrees
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) .build/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

web: pickle

json:
	mkdir -p .build/json .build/doctrees
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) .build/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	mkdir -p .build/htmlhelp .build/doctrees
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) .build/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in .build/htmlhelp."

latex: pdf-figures
	mkdir -p .build/latex .build/doctrees
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) .build/latex
	@echo
	@echo "Build finished; the LaTeX files are in .build/latex."
	@echo "Run \`make all-pdf' or \`make all-ps' in that directory to" \
	      "run these through (pdf)latex."

pdf: latex
	cd .build/latex && make all-pdf
	@echo
	@echo "Your PDF is available in .build/latex"

changes:
	mkdir -p .build/changes .build/doctrees
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) .build/changes
	@echo
	@echo "The overview file is in .build/changes."

linkcheck:
	mkdir -p .build/linkcheck .build/doctrees
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) .build/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in .build/linkcheck/output.txt."

release: html pdf
	cd .build/html && tar czf ../../hforge-docs-html-$(GIT_VERSION).tgz *
	${EPYDOC} -o itools-reference-$(DATE) ${ITOOLS_PATH}/*/__init__.py
	tar -czhf itools-reference-$(DATE).tgz itools-reference-$(DATE)
	rm -rf itools-reference-$(DATE)

	${EPYDOC} --pdf -o itools-reference-pdf ${ITOOLS_PATH}/*/__init__.py
	mv itools-reference-pdf/api.pdf .build/latex/itools-reference.pdf
	rm -rf itools-reference-pdf
	cd .build/latex && tar czf ../../hforge-docs-pdf-$(GIT_VERSION).tgz \
										 itools-tutorial.pdf user-guide.pdf \
										 administrator-guide.pdf i18n.pdf git.pdf \
										 style.pdf packaging.pdf windows.pdf itools-reference.pdf

	cd itools && tar czf ../itools-examples-$(GIT_VERSION).tgz examples

	@echo
	@echo "***** SUMMARY *****"
	@echo "html doc is available ./hforge-docs-html-$(GIT_VERSION).tgz and"
	@echo "pdf doc is available ./hforge-docs-pdf-$(GIT_VERSION).tgz"
	@echo "itools-examples is available ./itools-examples-$(GIT_VERSION).tgz"
	@echo "itools-reference is available ./itools-reference-$(DATE).tgz"


