from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import EmbeddingRetriever

from src.utils.constants import EMBEDDING_MODEL, RETRIEVED_DOCUMENTS


def get_retriever(document_store: InMemoryDocumentStore) -> EmbeddingRetriever:
    return EmbeddingRetriever(
        document_store=document_store,
        embedding_model=EMBEDDING_MODEL,
        use_gpu=False,
        top_k=RETRIEVED_DOCUMENTS,
    )
