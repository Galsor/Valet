import streamlit as st
from haystack.pipelines import Pipeline

from src.pipeline.answer_check import get_veracity_node
from src.pipeline.answer_generator import get_answer_generator
from src.pipeline.document_store import load_document_store
from src.pipeline.retriever import get_retriever

@st.cache_resource
def load_QA_pipeline() -> Pipeline:
    document_store = load_document_store()

    retriever = get_retriever(document_store)
    generator = get_answer_generator()
    veracity = get_veracity_node()


    pipe = Pipeline()
    pipe.add_node(component=retriever, name="Retriever", inputs=["Query"])
    pipe.add_node(component=generator, name="Generator", inputs=["Retriever"])
    pipe.add_node(component=veracity, name="Veracity", inputs=["Generator"])
    return pipe
