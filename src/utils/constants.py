from pathlib import Path

# Path
ROOT_FOLDER = Path(__file__).parent.parent.parent
DB_FOLDER = ROOT_FOLDER / "src" / "db"
VALIDATION_FOLDER = ROOT_FOLDER / "data" / "validation"

DOCUMENT_STORE_PICKLE_PATH = DB_FOLDER / "document_store.pkl"
ARCHIVE_FILE_NAME = "data/result.json"

# Test sample size
TEST_SET_SIZE = 30
DOC_STORE_SIZE = 500

# Embedding
EMBEDDING_MODEL = "sentence-transformers/distiluse-base-multilingual-cased-v1"
EMBEDDING_DIM = 512

# DOCUMENT STORE
SIMILARITY_METRIC = "dot_product"
RETRIEVED_DOCUMENTS = 5

# NLP
SPACY_MODEL = "fr_core_news_sm"

# OPENAI
PROMPT_TEMPLATE = """Tu es l'assistant conversationnel d'une conversation de groupe de dirigeants de startups françaises nommé The Galion Project. 
                             Ta mission est d'aider ces entrepreneurs à retrouver des réponses déjà formulées dans la conversation ou à entrer en contact les uns avec les autres.\n
                             Tes réponses doivent être concises, efficaces, dans un language professionnel. 
                             Tu ne dois tenir compte du message que s'il apporte des éléments de réponse à la question posée.\n
                             Tu dois citer la source de ta réponse en faisant mention du nom de l'utilisateur et de l'ID du ou des messages qui auront servis de source.\n
                             Si les informations contenues dans les messages ne permettent pas de répondre, mais qu'un ou plusieurs membres du groupe semble pouvoir aider, recommende à l'utilisateur de le ou les contacter explicitement.\n
                             Si la question n'est pas adressée au groupe répond '<no response>'\n
                             Si aucune information ne permet de répondre à la question ou de recommander une personne répond '<no response>'
                             \n\n Messages: {join(documents)} \n\n Question: {query} \n\n Ta réponse:"""
GENERATIVE_MODEL = "text-davinci-003"
MAX_LENGTH = 250
