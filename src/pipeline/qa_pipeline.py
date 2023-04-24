import streamlit as st
from haystack.pipelines import GenerativeQAPipeline

from src.pipeline.answer_generator import get_answer_generator
from src.pipeline.document_store import load_document_store
from src.pipeline.retriever import get_retriever


@st.cache_resource
def load_business_glossary_QA_pipeline() -> GenerativeQAPipeline:
    document_store = load_document_store()

    retriever = get_retriever(document_store)

    generator = get_answer_generator()

    pipe = GenerativeQAPipeline(generator=generator, retriever=retriever)
    return pipe
