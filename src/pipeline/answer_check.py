from typing import Dict, List, Optional, Union

from haystack import Answer, BaseComponent
from haystack.nodes import PromptModel, PromptNode

from src.utils.constants import GENERATIVE_MODEL, ANSWER_CHECK_TEMPLATE, ANSWER_CHECK_TEMPERATURE, ANSWER_THE_QUESTION_TEMPLATE
from src.utils.vault import get_openai_secret


class VeracityNode(BaseComponent):
    outgoing_edges = 1

    def __init__(
        self,
        model_name_or_path: Union[str, PromptModel],
        api_key: Optional[str] = None,
        model_kwargs: Optional[Dict] = None,
        override_answer: Optional[str] = "<no response>",
    ):
        """
        Creates a VeracityNode

        :param model_name_or_path: The name of the model to use or an instance of the PromptModel.
        :param api_key: The API key to use for the model.
        :param model_kwargs: Additional keyword arguments passed when loading the model specified in `model_name_or_path`.
        """
        super().__init__()
        self.api_key = api_key
        self.model_name_or_path = model_name_or_path
        self.model_kwargs = model_kwargs
        self.override_answer = override_answer

    def run(
        self,
        query: str,
        answers: Optional[List[Answer]] = None,
        **kwargs,
    ):
        """
        Runs the fact checking. It asks the given model whether the given query is answered by the given context which
        are passed in results.

        :param query: The query to answer
        :param results: The given context
        :param kwargs: Additional keyword arguments, which will be passed as-is
        :return: The given query and context if the answer was correct, otherwise the given query a message that the answer
        was incorrect.
        """
        if query is None:
            return ValueError("query is None")
        if answers is None:
            return ValueError("answers is None")

        output_dict = {"query": query, "generated_answers": answers}
        output_dict.update(kwargs)

        validated_answers = [self.check_answer(query, answer) for answer in answers]

        output_dict["answers"] = validated_answers
        return output_dict, "output_1"

    def run_batch(
        self, queries: List[str], answers: Optional[List[List[Answer]]] = None, **kwargs
    ):
        """
        Runs VeracityNode in batch mode.

        :param queries: The queries to answer
        :param answers: The given answers
        :param kwargs: Additional keyword arguments, which will be passed as-is
        :return: The given queries and answers if the answers were correct, otherwise the given queries and a message that the answers
        were incorrect.
        """
        if queries is None:
            return ValueError("queries is None")
        if answers is None:
            return ValueError("answers is None")

        output_dict = {"queries": queries, "generated_answers": answers}
        output_dict.update(kwargs)

        validated_answers = []
        for query, answer in zip(queries, answers):
            validated_answers.append(
                [self.check_answer(query, answer) for answer in answer]
            )

        output_dict["answers"] = validated_answers
        return output_dict, "output_1"

    def check_answer(self, query: str, answer: Answer):
        """
        Checks whether the given answer is correct for the given query.
        - if the answer is correct, the answer is returned as-is.
        - if the answer contains <no response>, the answer is overwritten with the override_answer.
        - if the answer classified as incorrect by a PromptNode classifier, the answer is overwritten with the override_answer.
        
        :param query: The query to answer
        :param answer: The answer to check
        :return: The given answer if it is correct, otherwise a message that the answer was incorrect.
        """
        checked_answer = Answer(**answer.to_dict())
        if "<no response>" in answer.answer.lower():
            checked_answer.answer = self.override_answer
            return checked_answer
        else:
            has_found_answer = self.zero_shot_has_found_an_answer(query, answer)
            checked_answer.meta["has_found_answer"] = has_found_answer
            is_answering = self.zero_shot_answering_the_question(query, answer)
            checked_answer.meta["is_anwersing"] = is_answering
            
            if has_found_answer and is_answering:
                # No transformation needed
                return checked_answer
            else:
                # Overwrite answer with <no response>
                checked_answer.answer = self.override_answer
                return checked_answer

    def zero_shot_answering_the_question(self, query: str, answer: Answer)-> str:
        """
        Use generative model to check whether the given answer is correct for the given query.

        :param query: The query to answer
        :param answer: The answer to check
        :return: The answer of the model, expected to be either 'OUI' or 'NON'.
        """
        result_from_prompt_node = self.zero_shot_task(ANSWER_CHECK_TEMPLATE, query, answer)
        return "oui" in result_from_prompt_node.lower()
        

    def zero_shot_has_found_an_answer(self, query: str, answer: Answer) -> str:
        """
        Use generative model to check whether the the model found an answer to the question.

        :param query: The query to answer
        :param answer: The answer to check
        :return: The answer of the model, expected to be either 'OUI' or 'NON'.
        """
        result_from_prompt_node = self.zero_shot_task(ANSWER_THE_QUESTION_TEMPLATE, query, answer)
        return "oui" in result_from_prompt_node.lower()

    

    def zero_shot_task(self, prompt_template: str, query: str, answer: Answer) -> str:
        prompt = prompt_template.format(query=query, answer=answer.answer)
        prompt_node = PromptNode(
            model_name_or_path=self.model_name_or_path,
            api_key=self.api_key,
            model_kwargs=self.model_kwargs,
        )
        result_from_prompt_node: List[str] = prompt_node(prompt)
        return result_from_prompt_node[0]
    


def get_veracity_node() -> VeracityNode:
    """
    Returns a VeracityNode with the default model.
    """
    return VeracityNode(
        model_name_or_path=GENERATIVE_MODEL, api_key=get_openai_secret(), model_kwargs={"temperature": ANSWER_CHECK_TEMPERATURE}
    )
