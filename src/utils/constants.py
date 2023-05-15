from pathlib import Path

# Path
ROOT_FOLDER = Path(__file__).parent.parent.parent
DB_FOLDER = ROOT_FOLDER / "src" / "db"
VALIDATION_FOLDER = ROOT_FOLDER / "data" / "validation"

DOCUMENT_STORE_PICKLE_PATH = DB_FOLDER / "document_store.pkl"
ARCHIVE_FILE_NAME = "data/result.json"
PRESTA_ARCHIVE_FILE_NAME = "data/result prestas.json"

# Test sample size
TEST_SET_SIZE = 30
DOC_STORE_SIZE = 3000

# Embedding
EMBEDDING_MODEL = "sentence-transformers/distiluse-base-multilingual-cased-v1"
EMBEDDING_DIM = 512

# DOCUMENT STORE
SIMILARITY_METRIC = "dot_product"
RETRIEVED_DOCUMENTS = 7

# NLP
SPACY_MODEL = "fr_core_news_sm"

# OPENAI
PROMPT_TEMPLATE = """Ta mission est d'aider les membres d'un groupe Telegram nommé le Galion.\n
                             Lorsqu'un membre pose une question au groupe tu essaieras de répondre de manière étayée en te basant sur la sélection de messages ci-dessous.
                             Tu ne dois tenir compte du message que s'il répond à la question posée.\n
                             Pour chaque élément de réponse, tu dois citer les noms des utilisateurs qui auront fournit l'information.\n
                             Tu ne dois pas inventer d'information supplémentaire.\n
                             Si les informations contenues dans les messages ne permettent pas de répondre, mais qu'un ou plusieurs membres du groupe peuvent aider, recommende à l'utilisateur de le ou les contacter.\n
                             Tu ne dois répondre qu'aux questions adressées au groupe.\n
                             Si tu ne peux pas répondre à la question répond '<no response>'\n
                             \n\n Messages: {join(documents)} \n\n Question: {query} \n\n Ta réponse:"""
GENERATIVE_MODEL = "gpt-3.5-turbo"
MAX_LENGTH = 500
