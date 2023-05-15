import logging
import re
import pprint 

import streamlit as st
from haystack import Document

from src.pipeline.qa_pipeline import load_QA_pipeline
from src.utils.formatter import reverse_formatting

logger = logging.getLogger(__name__)


def clear_submit():
    st.session_state["submit"] = False


def display_ask_tab():
    query = st.text_area(
        "**Ask any question to the Galion's Community:**",
        help="Ask a question as if you were writing in a Telegram conversation. French is highly recommended.",
        on_change=clear_submit,
    )
    button = st.button("🧠 Generate anwser")
    if button or st.session_state.get("submit"):
        if not query:
            st.error("Please enter a question!")
        else:
            st.session_state["submit"] = True
            display_model_answer_and_sources(query)


def display_model_answer_and_sources(query: str):
    answer_col, sources_col = st.columns(2)
    try:
        pipe = load_QA_pipeline()
        logger.info(f"Question asked: {query}")
        results = pipe.run(query)
        answer = results["answers"][0].answer
        logger.info(f"Generated answer: {answer}")
        sources_documents = results["documents"]

        with answer_col:
            st.markdown("#### Answer")
            st.markdown(f"> 💬 {format_answer_in_markdown(answer)}")
        with sources_col:
            st.markdown("#### Documents")
            for doc in sources_documents:
                display_recommended_document(doc)

    except Exception as e:
        st.error(repr(e))


def format_answer_in_markdown(answer: str) -> str:
    return re.sub(r"\s?(\[.*\])$", r"  \n   > _\1_", answer.rstrip())


def display_recommended_document(doc: Document):
    doc_content = reverse_formatting(doc.content)
    logger.info("Document retrieved:\n" + pprint.pformat(doc_content))
    with st.expander("📰 " + doc_content["from"]):
        del doc_content["from"]
        for key, value in doc_content.items():
            st.markdown(f"**{key.capitalize()}**: {value}")
