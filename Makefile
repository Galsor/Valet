SHELL := /bin/bash

document_store:
	python -c "from src.pipeline.document_store import save_document_store; save_document_store()"


lint:
	python -m black .
	python -m isort .

app:
	python -m streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false

validation:
	python -c "from tests.integration.responses import build_validation_results; build_validation_results(label='$(if $(label),$(label),)')"

unit_test:
	python -m pytest tests/unit
