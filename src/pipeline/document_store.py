import logging
import os
import pickle
from typing import Optional

import streamlit as st
from haystack import Document
from haystack.document_stores import InMemoryDocumentStore

from src.pipeline.data import get_raw_conversation_store
from src.pipeline.retriever import get_retriever
from src.utils.constants import (DOCUMENT_STORE_PICKLE_PATH, EMBEDDING_DIM,
                                 SIMILARITY_METRIC)
from src.utils.formatter import format_messages

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
    formated_messages = format_messages(messages)
    document_store = InMemoryDocumentStore(
        similarity=SIMILARITY_METRIC, embedding_dim=EMBEDDING_DIM
    )
    document_store.write_documents(
        [
            Document(id=id, content=message, id_hash_keys=["content"])
            for id, message in formated_messages.items()
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
