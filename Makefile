# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = MAB-VLSI
SOURCEDIR     = docs/source
BUILDDIR      = docs/build
TEST_PATH     = ./tests

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean-py:
	find . -name '*.pyc' -exec rm {} + 
	find . -name '*.pyo' -exec rm {} +
	find . -name '*.tmp' -exec rm {} \;

clean-build: 
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-doc:
	rm -rf $(BUILDDIR)/*

clean: clean-py clean-build clean-doc
	
isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint:
	flake8 --exclude=.tox

test: clean
	py.test --cov=mab --verbose --color=yes $(TEST_PATH)

run: clean
	python run.py
	
.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
