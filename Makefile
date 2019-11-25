.PHONY: help sdist datamaestro datamaestro_ml

help:
	@echo "Commands are: sdist "

sdist: datamaestro datamaestro_ml
	@echo "Done..."

datamaestro_ml:
	cd $@; rm dist/*; python3 setup.py sdist && twine upload --username bpiwowar --skip-existing  dist/*

datamaestro:
	cd $@; rm dist/*; python3 setup.py sdist && twine upload --username bpiwowar --skip-existing  dist/*
