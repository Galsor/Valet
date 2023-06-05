import streamlit as st
from haystack.nodes import Shaper
from haystack.nodes.prompt import PromptNode
from haystack.pipelines import Pipeline

from src.pipeline.answer_check import get_veracity_node
from src.pipeline.answer_generator import get_answer_generator
from src.pipeline.doc_check import get_validate_documents_node
from src.pipeline.document_store import load_document_store
from src.pipeline.rephrase import get_answer_rephraser_node
from src.pipeline.retriever import get_retriever
from src.pipeline.rephrase import get_answer_rephraser_node
from src.pipeline.check import get_validate_documents_node
from src.pipeline.doc_duplicate import DuplicateDocQueryNode

@st.cache_resource
def load_QA_pipeline() -> Pipeline:
    document_store = load_document_store()

    retriever = get_retriever(document_store)
    generator = get_answer_generator()
    veracity = get_veracity_node()


    pipe = Pipeline()
    pipe.add_node(component=retriever, name="Retriever", inputs=["Query"])
    pipe.add_node(component=DuplicateDocQueryNode(), name="DuplicateDocQuery", inputs=["Retriever"])
    pipe.add_node(component=generator, name="Generator", inputs=["DuplicateDocQuery"])
    pipe.add_node(component=veracity, name="Veracity", inputs=["Generator"])
    return pipe
