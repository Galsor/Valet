import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from src.pipeline.data import get_test_conversations
from src.pipeline.qa_pipeline import load_QA_pipeline
from src.utils.constants import ROOT_FOLDER
from src.utils.formatter import get_raw_text
from src.utils.nlp import is_question
from src.utils.type import MessageList

logger = logging.getLogger(__name__)


def is_json_serializable(obj: Any) -> bool:
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False


def prepare_results_for_json(
    results: Union[Dict, List[Dict]]
) -> Union[Dict, List[Dict]]:
    if isinstance(results, dict):
        processed_results = {}
        for key, value in results.items():
            processed_results[key] = prepare_results_for_json(value)
        return processed_results
    elif isinstance(results, list):
        processed_results = []
        for result in results:
            processed_results.append(prepare_results_for_json(result))
        return processed_results
    elif is_json_serializable(results):
        return results
    elif hasattr(results, "to_dict"):
        return results.to_dict()
    elif hasattr(results, "to_json"):
        return results.to_json()
    else:
        logger.warning(f"Could not serialize: {results}")
        return None


def save_results_as_json(results: List[Dict], label: str):
    filename = f"{label}_{datetime.now().strftime('%Y%m%d_%H_%M')}.json"
    with open(ROOT_FOLDER / f"data/validation/{filename}", "w") as f:
        json_results = prepare_results_for_json(results)
        json.dump(json_results, f)


def collect_results(
    pipeline, test_set: MessageList, save: bool, label: str
) -> List[Dict]:
    results = []
    i = 0
    for message in test_set:
        raw_message = get_raw_text(message)
        if is_question(raw_message):
            i += 1
            logger.info(f"[{i}] Processing: {raw_message}")
            try:
                answer = pipeline.run(raw_message)
                results.append(answer)
            except Exception as e:
                if save:
                    save_results_as_json(results, "failed_" + label)
                raise e
    if save:
        save_results_as_json(results, label)
    return results


def build_validation_results(
    save: bool = True, label: Optional[str] = "validation"
) -> List[Dict]:
    test_set = get_test_conversations()
    pipeline = load_QA_pipeline()
    results = collect_results(pipeline, test_set, save, label)
    return results
