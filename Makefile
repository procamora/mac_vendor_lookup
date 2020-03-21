#!/usr/bin/env make
# -*- coding: utf-8 -*-

OUTPUT_EGG=procamora_mac_vendor_lookup.egg-info/
OUTPUT_DIST=dist/
OUTPUT_MANIFEST=MANIFEST


# python3 -m pip install --user --upgrade setuptools wheel twine


all: clean dist git upload


dist:
	python3 setup.py sdist


#https://twine.readthedocs.io/en/latest/
upload:
	twine upload dist/* -u procamora --verbose


git:
	git add .
	git commit -m "update from Makefile"
	git push


clean:
	[ ! -d $(OUTPUT_EGG) ] || rm -rf $(OUTPUT_EGG)
	[ ! -d $(OUTPUT_DIST) ] || rm -rf $(OUTPUT_DIST)
	[ ! -f $(OUTPUT_MANIFEST) ] || rm -f $(OUTPUT_MANIFEST)


.PHONY: dist clean git upload all