import json

import streamlit as st

from src.utils.constants import *


def display_model_card_tab():
    model_card = get_model_card()
    st.json(model_card)


def get_model_card() -> str:
    return json.dumps(
        {
            "Question detection": {"librairy": "Spacy", "model": SPACY_MODEL},
            "Sentences embedding": {
                "library": "HuggingFace Transformers",
                "model": EMBEDDING_MODEL,
                "embedding dimensions": EMBEDDING_DIM,
            },
            "Vectors storage": {
                "db": "In Memory",
                "similarity_metric": SIMILARITY_METRIC,
                "retrieved documents": RETRIEVED_DOCUMENTS,
            },
            "Answer generation": {
                "library": "openai",
                "model": GENERATIVE_MODEL,
                "max_response_length": MAX_LENGTH,
            },
        }
    )
