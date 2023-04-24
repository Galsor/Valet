SHELL := /bin/bash

venv:
	source .venv/bin/activate

build_document_store: venv
	python src/pipeline/document_store.py