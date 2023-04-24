from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import EmbeddingRetriever


def get_retriever(document_store: InMemoryDocumentStore) -> EmbeddingRetriever:
    return EmbeddingRetriever(
        document_store=document_store,
        embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
        use_gpu=True,
        top_k=5,
    )