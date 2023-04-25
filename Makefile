SHELL := /bin/bash

document_store:
	python -c "from src.pipeline.document_store import save_document_store; save_document_store()"


lint:
	python -m black .
	python -m isort .

app:
	python -m streamlit run app.py