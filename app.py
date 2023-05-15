import logging

import streamlit as st

from src.app.ask_page import display_ask_tab
from src.app.model_card_page import display_model_card_tab
from src.app.validation_page import display_validation_tab
from src.pipeline.qa_pipeline import load_QA_pipeline

st.title("The Galion's project")


def run():
    display_sidebar()
    ask_tab, validation_tab, model_card_tab = st.tabs(
        ["💬 Ask a question", "🧪 Explore validation", "📇 Model card"]
    )
    with ask_tab:
        display_ask_tab()
    with validation_tab:
        display_validation_tab()
    with model_card_tab:
        display_model_card_tab()


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
