from haystack.nodes.prompt import (AnswerParser, PromptModel, PromptNode,
                                   PromptTemplate)

from src.utils.constants import GENERATIVE_MODEL, MAX_LENGTH, REPHRASE_TEMPLATE
from src.utils.vault import get_openai_secret


def get_answer_rephraser_node() -> PromptNode:
    prompt_open_ai = PromptModel(
        model_name_or_path=GENERATIVE_MODEL,
        max_length=MAX_LENGTH,
        api_key=get_openai_secret(),
    )
    rephrase_prompt = PromptTemplate(
        name="rephrase",
        prompt_text=REPHRASE_TEMPLATE,
        output_parser=AnswerParser(),
    )
    return PromptNode(prompt_open_ai, default_prompt_template=rephrase_prompt)
