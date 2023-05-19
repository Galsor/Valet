SHELL := /bin/bash

local_document_store:
	python -c "from src.pipeline.document_store import save_document_store; save_document_store()"

pinecone:
	python -c "from src.pipeline.document_store import build_document_store; build_document_store(doc_store_type ='pinecone')"

lint:
	python -m black .
	python -m isort .

app:
	python -m streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false

validation:
	python -c "from tests.integration.responses import build_validation_results; build_validation_results(label='$(if $(label),$(label),validation)')"

cherry_validation:
	python -c "from tests.integration.responses import build_validation_base_de_test; build_validation_base_de_test()"

unit_test:
	python -m pytest tests/unit