from pathlib import Path

from src.utils.type import DocumentStore

# Path
ROOT_FOLDER = Path(__file__).parent.parent.parent
DB_FOLDER = ROOT_FOLDER / "src" / "db"
VALIDATION_FOLDER = ROOT_FOLDER / "data" / "validation"

DOCUMENT_STORE_PICKLE_PATH = DB_FOLDER / "document_store.pkl"
ARCHIVE_FILE_NAME = "data/result.json"
PRESTA_ARCHIVE_FILE_NAME = "data/result prestas.json"

# Document Store
DOCUMENT_STORE_TYPE = DocumentStore.PINECONE
PINECONE_ENVIRONMENT = "us-east4-gcp"
INDEX_NAME = "valet-index"
DOC_STORE_SIZE = 1e6


# Test sample size
TEST_SET_SIZE = 30

# Embedding
EMBEDDING_MODEL = "sentence-transformers/distiluse-base-multilingual-cased-v1"
EMBEDDING_DIM = 512

# DOCUMENT STORE
SIMILARITY_METRIC = "cosine"
RETRIEVED_DOCUMENTS = 5

# NLP
SPACY_MODEL = "fr_core_news_sm"

# Answer generation
GENERATIVE_MODEL = "gpt-3.5-turbo"
MAX_LENGTH = 500
PROMPT_TEMPLATE = """Consignes:
--------
- Réponds à l'utilisateur sur la base des informations partagés par les autres utilisateurs. 
- N'ajoute pas d'information. 
- Ta réponse doit être factuelle
- Ne répond que si les messages contiennent la réponse à la question.
- Ne répond à cette demande que si elle est adressée à l'entièreté du groupe.
- Tu mentionneras les utilisateurs qui auront fournit les éléments de réponse.
- Si les informations présentes dans les messages retrouvés ne permettent pas de fournir une réponse précise, répond impérativement et uniquement la mention suivante: <no response>.
- Ne prend pas en compte les examples ci dessous dans ta réponse
EXAMPLE
========
Messages:
--------
- From: Yohan BENTOLILA
- ID: 20055
- In response to: [20053] Julien MARDAS: Petite question rapide, je suis sûr que beaucoup d'entre vous utilisent des outils de roadmap produit (le contraire serait fou)Je fais un petit sondage, qu'est-ce que vous utilisez ?
- Message: Jira propose désormais une option roadmap qu on utilise pour le quotidien. Pour des présentations internes ou externes on est sur du slide. 
---
- From: Virgile RAINGEARD
- ID: 20057
- In response to: [20053] Julien MARDAS: Petite question rapide, je suis sûr que beaucoup d'entre vous utilisent des outils de roadmap produit (le contraire serait fou)Je fais un petit sondage, qu'est-ce que vous utilisez ?
- Message: https://www.cycle.app/ 
---
- From: Alexis TEPLITCHI
- ID: 20087
- Date: 2023-02-23T17:38:42
- In response to: [20053] Julien MARDAS: Petite question rapide, je suis sûr que beaucoup d'entre vous utilisent des outils de roadmap produit (le contraire serait fou)Je fais un petit sondage, qu'est-ce que vous utilisez ?
- Message: https://harvestr.io/fr/ 
---
Demande:
--------
Hello les Galion, Est-ce que vous auriez des outils de roadmap produit à me conseiller?
Réponse:
--------
Voici quelques outils de roadmap produit recommandés par les membres du Galion:
- Jira propose une option roadmap (@Yohan BENTOLILA)
- Cycle (@Virgile RAINGEARD)
- Harvestr (@Alexis TEPLITCHI)
========
EXAMPLE
=======
Voici quelques outils de roadmap produit recommandés par les membres du Galion:- Jira propose une option roadmap (@Yohan BENTOLILA)- Cycle (@Virgile RAINGEARD)- Harvestr (@Alexis TEPLITCHI)

Messages:
--------
- From: John CIAVARELLA
- ID: 13683
- Message: Hello à tous, quel package pour un VP Europe ?
---
- From: Franck ROUGEAU
- ID: 11424
- Message: Hello les Galions, quelqu'un connait-il Hubert Patural, chairman OCBI, comme investisseur ?
---
Demande:
--------
Quelqu'un connaitrait un bon avocat en droit des affaires?
Réponse:
--------
<no response>
========

Messages:
--------
{join(documents)}
Demande:
--------
{query}
Réponse:
--------
"""

# Answer check
ANSWER_CHECK_TEMPLATE = """
                Message entrant:
                {query}
                Réponse suggérée:
                {answer}
                Est-ce que cette réponse répond factuellemment à la question et est susceptible d'aider l'utilisateur ? 
                Répondez par OUI ou par NON et rien d'autre.
                """


REPHRASE_TEMPLATE = """Consignes:
- Supprime les passages où l'algorithme ne répond pas factuellement à question.
- Conserve les autres informations contenues dans la réponse notamment les références aux personnes et aux ID de messages.
- Ne rajoute pas d'information
- Si la réponse générée est '<no response>', la réponse corrigée doit impérativement être également <no response>. 
Question posée:
'{query}'
Réponse générée par l'algorithme:
'{generated_answers[0].answer}'
Réponse corrigée:
"""
DOC_RELEVANCE_CHECK_TEMPLATE = """Question:
'{query}'
Messages retrouvés:
'{'- '.join(['['+ doc.id + '] ' + doc.content for doc in documents])}'
Consigne:
Liste les ID des messages qui pourrait permettre de répondre à la question posée 
Format attendu de la réponse: [1], [34], [4].
Documents:
"""
