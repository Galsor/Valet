import logging
import os
import pickle
from typing import Optional

import streamlit as st
from haystack import Document
from haystack.document_stores import (BaseDocumentStore, InMemoryDocumentStore,
                                      PineconeDocumentStore)

from src.pipeline.data import get_raw_conversation_store
from src.pipeline.retriever import get_retriever
from src.utils.constants import (DOCUMENT_STORE_PICKLE_PATH,
                                 DOCUMENT_STORE_TYPE, EMBEDDING_DIM,
                                 INDEX_NAME, PINECONE_ENVIRONMENT,
                                 SIMILARITY_METRIC)
from src.utils.formatter import format_messages
from src.utils.type import DocumentStore

logger = logging.getLogger(__name__)


def get_document_store(doc_store_type: Optional[DocumentStore] = DOCUMENT_STORE_TYPE):
    if doc_store_type == DocumentStore.LOCAL:
        return InMemoryDocumentStore(
            similarity=SIMILARITY_METRIC, embedding_dim=EMBEDDING_DIM
        )
    elif doc_store_type == DocumentStore.PINECONE:
        return PineconeDocumentStore(
            api_key=os.getenv("PINECONE_API_KEY"),
            index=INDEX_NAME,
            environment=PINECONE_ENVIRONMENT,
            similarity=SIMILARITY_METRIC,
            embedding_dim=EMBEDDING_DIM,
        )
    else:
        raise NotImplementedError()


@st.cache_resource
def load_document_store() -> BaseDocumentStore:
    if (
        DOCUMENT_STORE_TYPE == DocumentStore.LOCAL
        and DOCUMENT_STORE_PICKLE_PATH.exists()
    ):
        logger.info("Loading document store from file")
        document_store = load_document_store_from_local_pickle()
    elif DOCUMENT_STORE_TYPE == DocumentStore.PINECONE:
        document_store = get_document_store()
    else:
        logger.info("Building document store from source")
        document_store = build_document_store()
    return document_store


def build_document_store(
    doc_store_type: Optional[DOCUMENT_STORE_TYPE] = None,
) -> BaseDocumentStore:
    messages = get_raw_conversation_store()
    formated_messages = format_messages(messages)
    document_store = get_document_store()
    document_store.write_documents(
        [
            Document(id=id, content=message, id_hash_keys=["content"])
            for id, message in formated_messages.items()
        ],
        duplicate_documents="skip",
    )
    retriever = get_retriever(document_store)
    document_store.update_embeddings(retriever, update_existing_embeddings=False)
    return document_store


def load_document_store_from_local_pickle() -> BaseDocumentStore:
    with open(DOCUMENT_STORE_PICKLE_PATH, "rb") as pkl:
        document_store = pickle.load(pkl)
        if not isinstance(document_store, InMemoryDocumentStore):
            raise TypeError(
                f"Object loaded from pickle is not InMemoryDocumentStore but {type(document_store)}"
            )
    return document_store


def save_document_store(
    path: os.PathLike = DOCUMENT_STORE_PICKLE_PATH,
    document_store: Optional[BaseDocumentStore] = None,
):
    if document_store is None:
        document_store = build_document_store()
    with open(path, "wb") as pkl:
        pickle.dump(document_store, pkl)
