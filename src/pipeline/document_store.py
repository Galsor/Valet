import json
import logging
import os
import pickle
from typing import Optional

import streamlit as st
from haystack import Document
from haystack.document_stores import InMemoryDocumentStore

from src.pipeline.data import get_raw_conversation_store
from src.pipeline.retriever import get_retriever
from src.utils.constants import DOCUMENT_STORE_PICKLE_PATH

logger = logging.getLogger(__name__)


@st.cache_resource
def load_document_store() -> InMemoryDocumentStore:
    if DOCUMENT_STORE_PICKLE_PATH.exists():
        logger.info("Loading document store from file")
        document_store = load_document_store_from_local_pickle()
    else:
        logger.info("Building document store from source")
        document_store = build_document_store()
    return document_store


def build_document_store() -> InMemoryDocumentStore:
    messages = get_raw_conversation_store()
    document_store = InMemoryDocumentStore(similarity="cosine")
    document_store.write_documents(
        [
            Document(
                id=message["id"], content=json.dumps(message), id_hash_keys=["content"]
            )
            for message in messages
        ]
    )
    retriever = get_retriever(document_store)
    document_store.update_embeddings(retriever)
    return document_store


def load_document_store_from_local_pickle() -> InMemoryDocumentStore:
    with open(DOCUMENT_STORE_PICKLE_PATH, "rb") as pkl:
        document_store = pickle.load(pkl)
        if not isinstance(document_store, InMemoryDocumentStore):
            raise TypeError(
                f"Object loaded from pickle is not InMemoryDocumentStore but {type(document_store)}"
            )
    return document_store


def save_document_store(
    path: os.PathLike = DOCUMENT_STORE_PICKLE_PATH,
    document_store: Optional[InMemoryDocumentStore] = None,
):
    if document_store is None:
        document_store = build_document_store()
    with open(path, "wb") as pkl:
        pickle.dump(document_store, pkl)


if __name__ == "__main__":
    import os
    from pathlib import Path

    os.chcwd(Path(__file__).parent.parent.parent)
    save_document_store()
