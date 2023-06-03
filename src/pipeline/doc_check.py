from haystack.nodes import Shaper
from haystack.nodes.prompt import (AnswerParser, PromptModel, PromptNode,
                                   PromptTemplate)

from src.utils.constants import (DOC_RELEVANCE_CHECK_TEMPLATE,
                                 GENERATIVE_MODEL, MAX_LENGTH)
from src.utils.vault import get_openai_secret


def get_validate_documents_node() -> PromptNode:
    prompt_open_ai = PromptModel(
        model_name_or_path=GENERATIVE_MODEL,
        max_length=MAX_LENGTH,
        api_key=get_openai_secret(),
    )
    doc_relevance_prompt = PromptTemplate(
        name="document_check",
        prompt_text=DOC_RELEVANCE_CHECK_TEMPLATE,
        output_parser=AnswerParser(reference_pattern=r"\[(\d+)\]"),
    )
    return PromptNode(
        prompt_open_ai,
        default_prompt_template=doc_relevance_prompt,
        output_variable="relevant_doc_ids",
    )
