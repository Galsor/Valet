import spacy

from src.utils.constants import SPACY_MODEL

nlp = spacy.load(SPACY_MODEL)


def is_question(text: str) -> bool:
    doc = nlp(text)
    is_question_mark_mask = [token.is_punct and token.text == "?" for token in doc]
    return any(is_question_mark_mask)
