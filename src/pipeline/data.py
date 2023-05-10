import json
from typing import Tuple

import pandas as pd

from src.utils.constants import (ARCHIVE_FILE_NAME, DOC_STORE_SIZE,
                                 TEST_SET_SIZE)
from src.utils.type import MessageList
from src.utils.nlp import is_question
from src.utils.formatter import get_raw_text

def get_conversations(filename: str = ARCHIVE_FILE_NAME) -> MessageList:
    raw_data = get_raw_conversations(filename)
    message_data = filter_by_type_message(raw_data)
    return message_data


def get_raw_conversations(
    filename: str = ARCHIVE_FILE_NAME,
) -> MessageList:
    conversations_path = filename
    with open(conversations_path, "r") as f:
        data = json.load(f)
    return data["messages"]


def filter_by_type_message(conversations: MessageList) -> MessageList:
    return [message for message in conversations if message["type"] == "message"]


def get_conversation_dataframe(conversations: MessageList) -> pd.DataFrame:
    return pd.DataFrame(conversations)


def get_questions(conversations: MessageList) -> MessageList:
    return [message for message in conversations if is_question(get_raw_text(message))]


def split_store_test_set(
    conversations: MessageList,
    n_test_questions: int = TEST_SET_SIZE,
    store_size: int = DOC_STORE_SIZE,
) -> Tuple[MessageList, MessageList]:
    """
    Split a list of conversations into a store and a test set.

    Parameters:
        conversations (MessageList): A list of conversation messages.

    Returns:
        Tuple[MessageList, MessageList]: A tuple containing the store and test set
            of conversation messages. The store set contains all messages in the
            original list except the last 30 questions, while the test set contains
            only the last 30 questions and their corresponding answers.

    This function creates a copy of the input conversation list and removes the
    last 30 questions and their answers from the store set.
    The store set is returned as the first element of the output tuple.
    The test set is created by appending the last 30 questions and their answers.
    It is returned as the second element of the output tuple.
    """
    last_30_questions = get_questions(conversations)[-n_test_questions - 1 : -1]
    first_test_questions_id = last_30_questions[0]["id"]

    for i, message in enumerate(reversed(conversations)):
        if message["id"] == first_test_questions_id:
            break

    start, end = get_store_indexes(conversations, store_size, i)
    raw_conversation_store, test_set = (
        conversations[start:end],
        conversations[-i:],
    )
    return raw_conversation_store, test_set


def get_store_indexes(
    conversations: MessageList, store_size: int, i: int
) -> Tuple[int, int]:
    last_store_conversion_index = len(conversations) - i
    if store_size > last_store_conversion_index:
        raise ValueError(f" Max store_size is {last_store_conversion_index}")
    first_store_conversation_index = last_store_conversion_index - store_size
    return first_store_conversation_index, last_store_conversion_index


def get_raw_conversation_store() -> MessageList:
    conversations = get_conversations()
    raw_conversation_store, _ = split_store_test_set(conversations)
    return raw_conversation_store


def get_test_conversations() -> MessageList:
    conversations = get_conversations()
    _, test_set = split_store_test_set(conversations)
    return test_set
