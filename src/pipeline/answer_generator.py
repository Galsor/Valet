from haystack.nodes import (AnswerParser, PromptModel, PromptNode,
                            PromptTemplate)

from src.utils.constants import GENERATIVE_MODEL, MAX_LENGTH, PROMPT_TEMPLATE
from src.utils.vault import get_openai_secret


def get_answer_generator() -> PromptNode:
    prompt_open_ai = PromptModel(
        model_name_or_path=GENERATIVE_MODEL,
        max_length=MAX_LENGTH,
        api_key=get_openai_secret(),
    )
    lfqa_prompt = PromptTemplate(
        name="lfqa",
        prompt_text=PROMPT_TEMPLATE,
        output_parser=AnswerParser(),
    )
    return PromptNode(prompt_open_ai, default_prompt_template=lfqa_prompt, output_variable="generated_answers")
