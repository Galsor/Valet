import re
from typing import Dict

from src.utils.type import Message, MessageList


def build_conversation_mapping(conversations: MessageList) -> Dict[int, Message]:
    return {m["id"]: m for m in conversations}


def get_raw_text(message: Message) -> str:
    txt = message["text"]
    if isinstance(txt, str):
        return txt
    elif isinstance(txt, list):
        raw_txt = ""
        for item in txt:
            if isinstance(item, str):
                raw_txt += item
            elif isinstance(item, dict):
                raw_txt += item["text"]
            else:
                raise NotImplementedError(
                    f"No parser implemented for {type(item)} submessage"
                )
        return raw_txt
    else:
        raise NotImplementedError(f"No get_raw_text method implemented for {type(txt)}")


def format_context_message(message: Message) -> str:
    return f"[{message['id']}] {message['from']}: {get_raw_text(message)}"


def stringify_message(message: Message) -> str:
    in_response = (
        "- In response to: " + message.get("context") + "\n"
        if "context" in message
        else ""
    )
    return f"- From: {message['from']}\n- ID: {message['id']}\n{in_response}- Message: {message['text']}\n---\n"



def format_messages(conversations: MessageList) -> Dict[int, str]:
    """Destructive formating"""
    conv_mapping = build_conversation_mapping(conversations)
    formated_messages = {}
    for message in conversations:
        # override formatted text
        message["text"] = get_raw_text(message)

        # Add ref to question
        if (
            "reply_to_message_id" in message
            and message.get("reply_to_message_id") in conv_mapping
        ):
            responded_message = conv_mapping[message["reply_to_message_id"]]
            message["context"] = format_context_message(responded_message)

        # delete unnecessary keys
        for key in [
            "type",
            "date_unixtime",
            "from_id",
            "reply_to_message_id",
            "text_entities",
            "edited",
            "edited_unixtime",
        ]:
            if key in message:
                del message[key]
        formated_messages[message["id"]] = stringify_message(message)
    return formated_messages


def reverse_formatting(document: str) -> Message:
    keys = ["From", "ID", "In response to", "message"]
    extracted_values = {}
    for key in keys:
        pattern = r"{}:(.*?)(?=-\s|$)".format(key)
        match = re.search(pattern, document, re.DOTALL)
        if match:
            value = match.group(1).strip().replace("--", "")
            extracted_values[key.lower()] = value

    return extracted_values
