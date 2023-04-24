import logging

import streamlit as st

from src.app.ask_page import display_ask_tab
from src.pipeline.qa_pipeline import load_QA_pipeline

st.title("Business Glossary AI")


def run():
    display_sidebar()
    with st.spinner("🥁 Initializing the application. Average duration: ⏱ 2 minutes. "):
        load_business_glossary_QA_pipeline()
    ask_tab, add_tab = st.tabs(["🔮 Ask a question", "✒️ Add an entry"])
    with ask_tab:
        display_ask_tab()
    with add_tab:
        display_add_tab()


def display_sidebar():
    with st.sidebar:
        st.markdown("# About")
        st.markdown(
            "📚 This app is a `DEMO` showcasing the possibilities of generative AI in a private data scope such as the Galion's private conversions"
        )
        st.markdown("---")
        st.markdown(
            "It aims to illustrate how recent AI breakthrough, showcased in popular"
            " applications like ChatGPT, can be leveraged to retrieve and extend answers provided by the Galion's Community"
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
