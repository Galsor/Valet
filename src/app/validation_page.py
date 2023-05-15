from typing import Dict, List

import pandas as pd
import streamlit as st

from src.pipeline.data import get_last_validation_data


def display_validation_tab():
    with st.expander("❔  About the validation"):
        st.markdown(
            """This page shows the answers provided by the model when new questions (not present in the database) are asked.\n 
These are **the last thirty questions** asked on the Telegram group. The model **ignores the answers** provided later by the members of the group.\n 
The mention `<no response>` indicates that the model deliberately did not want to answer the question due to:
- Lack of context
- Lack of information present in previous messages
- The question does not call for an answer (retoric question, question in response to a question, onomatopoeia etc.)"""
        )
    display_validation_data()


def display_validation_data():
    last_validation_data = get_last_validation_data()
    formatted_data = get_question_and_answer_from_validation_data(last_validation_data)
    st.table(formatted_data)


def get_question_and_answer_from_validation_data(
    validation_data: List[Dict],
) -> pd.DataFrame:
    questions = []
    answers = []
    for pipeline_response in validation_data:
        questions.append(pipeline_response.get("query"))
        answers.append(pipeline_response["answers"][0]["answer"])

    return pd.DataFrame({"Questions": questions, "Answers": answers})
