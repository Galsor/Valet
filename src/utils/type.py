from enum import Enum
from typing import Dict, List, Union

Message = Dict[str, Union[str, int, List[Dict[str, str]]]]
MessageList = List[Message]


class DocumentStore(str, Enum):
    LOCAL = "local"
    PINECONE = "pinecone"
