from typing import Dict, List, Union

import pytest

from src.utils.formatter import (build_conversation_mapping,
                                 format_context_message, format_messages,
                                 get_raw_text, reverse_formatting,
                                 )


@pytest.fixture
def conversations():
    return [
        {"id": 1, "from": "John", "date": "2022-05-09", "text": "Hello world!"},
        {
            "id": 2,
            "from": "Alice",
            "date": "2022-05-09",
            "text": [
                "Hi, ",
                {"text": "how are you? ", "bold": True},
                "I hope you are doing well!",
            ],
            "reply_to_message_id": 1,
        },
        {
            "id": 3,
            "from": "Bob",
            "date": "2022-05-09",
            "text": [
                "I'm doing great! ",
                {"text": "Thanks for asking. ", "italic": True},
                "How about you?",
            ],
            "reply_to_message_id": 2,
        },
    ]

@pytest.fixture
def formated_conversations():
    return [ 
        "- From: John\n- ID: 1\n- Message: Hello world!\n---\n",
        "- From: Alice\n- ID: 2\n- In response to: [1] John: Hello world!\n- Message: Hi, how are you? I hope you are doing well!\n---\n",
        "- From: Bob\n- ID: 3\n- In response to: [2] Alice: Hi, how are you? I hope you are doing well!\n- Message: I'm doing great! Thanks for asking. How about you?\n---\n",
    ]

def test_build_conversation_mapping(conversations):
    expected = {
        1: {"id": 1, "from": "John", "date": "2022-05-09", "text": "Hello world!"},
        2: {
            "id": 2,
            "from": "Alice",
            "date": "2022-05-09",
            "text": [
                "Hi, ",
                {"text": "how are you? ", "bold": True},
                "I hope you are doing well!",
            ],
            "reply_to_message_id": 1,
        },
        3: {
            "id": 3,
            "from": "Bob",
            "date": "2022-05-09",
            "text": [
                "I'm doing great! ",
                {"text": "Thanks for asking. ", "italic": True},
                "How about you?",
            ],
            "reply_to_message_id": 2,
        },
    }
    assert build_conversation_mapping(conversations) == expected


def test_get_raw_text():
    message1 = {"id": 1, "text": "Hello world!"}
    message2 = {
        "id": 2,
        "text": [
            "Hi, ",
            {"text": "how are you? ", "bold": True},
            "I hope you are doing well!",
        ],
    }
    message3 = {"id": 3, "text": 123}
    with pytest.raises(NotImplementedError):
        get_raw_text(message3)
    assert get_raw_text(message1) == "Hello world!"
    assert get_raw_text(message2) == "Hi, how are you? I hope you are doing well!"


def test_format_context_message():
    message = {
        "id": 2,
        "from": "Alice",
        "date": "2022-05-09",
        "text": [
            "Hi, ",
            {"text": "how are you? ", "bold": True},
            "I hope you are doing well!",
        ],
        "reply_to_message_id": 1,
    }
    assert (
        format_context_message(message)
        == "[2] Alice: Hi, how are you? I hope you are doing well!"
    )


def test_format_messages(conversations, formated_conversations):
    expected_result = {
        1: formated_conversations[0],
        2: formated_conversations[1],
        3: formated_conversations[2],
    }

    result = format_messages(conversations)

    for (res_key, res_val), (exp_key, exp_val) in zip(result.items(), expected_result.items()):
        assert res_key == exp_key
        assert res_val == exp_val

def test_reverse_formatting(conversations, formated_conversations):
    for message, formated_message in zip(conversations, formated_conversations):
        # Information destructed by formating
        del message["date"]
        message["message"] = message["text"]
        del message["text"]
        for key, value in message.items():
            message[key]=str(value)
            
        assert reverse_formatting(formated_message) == message
