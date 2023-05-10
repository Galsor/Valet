import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

from src.pipeline.data import get_test_conversations
from src.pipeline.qa_pipeline import load_QA_pipeline
from src.utils.constants import ROOT_FOLDER
from src.utils.formatter import get_raw_text
from src.utils.nlp import is_question
from src.utils.type import MessageList

logger = logging.getLogger(__name__)

def save_results_as_json(results: List[Dict], label: str):
    filename = f"{label}_{datetime.now().strftime('%Y%m%d_%H_%M')}.json"
    with open(ROOT_FOLDER / f"data/validation/{filename}", "wb") as f:
        json.dump(results, f)

def collect_results(pipeline, test_set: MessageList) -> List[Dict]:
    results = []
    i=0
    for message in test_set:
        raw_message = get_raw_text(message)
        if is_question(raw_message):
            i+=1
            logger.info(f"[{i}] Processing: {raw_message}")
            results.append(pipeline.run(raw_message))
    return results


def build_validation_results(
    save: bool = True, label: Optional[str] = None
) -> List[Dict]:
    test_set = get_test_conversations()
    pipeline = load_QA_pipeline()
    results = collect_results(pipeline, test_set)
    if save:
        save_results_as_json(results, label)
    return results
