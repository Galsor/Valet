import streamlit as st
from haystack.pipelines import Pipeline
from haystack.nodes.prompt import PromptNode


from src.pipeline.answer_generator import get_answer_generator
from src.pipeline.document_store import load_document_store
from src.pipeline.retriever import get_retriever
from src.pipeline.rephrase import get_answer_rephraser_node
from src.pipeline.check import get_validate_documents_node


@st.cache_resource
def load_QA_pipeline() -> Pipeline:
    document_store = load_document_store()

    retriever = get_retriever(document_store)
    #filter = get_validate_documents_node()
    generator = get_answer_generator()
    rephraser = get_answer_rephraser_node()

    pipe = Pipeline()
    pipe.add_node(component=retriever, name="Retriever", inputs=["Query"])
    pipe.add_node(component=generator, name="Generator", inputs=["Retriever"])
    #pipe.add_node(component=rephraser, name="Rephrase", inputs=["Generator"])
    return pipe
