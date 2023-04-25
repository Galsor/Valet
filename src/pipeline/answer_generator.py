from haystack.nodes import PromptTemplate, AnswerParser, PromptNode, PromptModel

from src.utils.vault import get_openai_secret


def get_answer_generator() -> PromptNode:
    
    prompt_open_ai = PromptModel(model_name_or_path="text-davinci-003", api_key=get_openai_secret())

    # Make PromptNode use the model:
    return PromptNode(prompt_open_ai).set_default_prompt_template("question-answering")

