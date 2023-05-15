import glob
import json
import logging
import os
from typing import Dict, List, Optional, Tuple

import pandas as pd

from src.utils.constants import (ARCHIVE_FILE_NAME, DOC_STORE_SIZE,
                                 PRESTA_ARCHIVE_FILE_NAME, TEST_SET_SIZE,
                                 VALIDATION_FOLDER)
from src.utils.formatter import get_raw_text
from src.utils.nlp import is_question
from src.utils.type import MessageList

logger = logging.getLogger(__name__)


def get_conversations(filename: str = ARCHIVE_FILE_NAME) -> MessageList:
    raw_data = get_raw_conversations(filename)
    message_data = filter_by_type_message(raw_data)
    return message_data


def get_raw_conversations(
    filename: str = ARCHIVE_FILE_NAME,
) -> MessageList:
    with open(filename, "r") as f:
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
        store_size = last_store_conversion_index
    first_store_conversation_index = last_store_conversion_index - store_size
    return first_store_conversation_index, last_store_conversion_index


def get_raw_conversation_store() -> MessageList:
    conversations = get_conversations(ARCHIVE_FILE_NAME)
    raw_conversation_store, _ = split_store_test_set(conversations)
    
    # Append presta data (excluded from tests)
    presta_conversation = get_conversations(PRESTA_ARCHIVE_FILE_NAME)
    return presta_conversation + raw_conversation_store


def get_test_conversations() -> MessageList:
    conversations = get_conversations()
    _, test_set = split_store_test_set(conversations)
    return test_set


def get_last_validation_data() -> Optional[List[Dict]]:
    # Get the list of JSON files in the folder
    file_pattern = os.path.join(VALIDATION_FOLDER, "validation_*.json")
    json_files = glob.glob(file_pattern)

    # Sort the JSON files by modification time in descending order
    sorted_files = sorted(json_files, key=os.path.getmtime, reverse=True)

    # Check if any JSON files exist
    if sorted_files:
        # Get the path of the most recently edited file
        most_recent_file = sorted_files[0]

        # Read the data from the JSON file
        with open(most_recent_file, "r") as file:
            data = json.load(file)
        return data
    else:
        logger.warning("No validation files found.")
        return None
