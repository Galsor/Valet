# The Galion's Valet
Valet is a project that demonstrates the power of generative AI for Open Q&A. This project sources its responses from Telegram conversations in a group named Galion's Project, using state-of-the-art machine learning techniques to generate natural-sounding answers to a wide range of questions.

With Valet, you can experience the cutting-edge of AI research and explore the potential of natural language processing for your own projects. The demonstrator provides a user-friendly interface for asking questions and receiving responses in real-time, giving you a glimpse into the exciting future of intelligent virtual assistants.

## Features:

- 🎇 State-of-the-art generative AI for Open Q&A
- 💬 Sources responses from Telegram conversations in a group named Galion's Project
- 🖱 User-friendly interface for asking questions and receiving responses in real-time

## Installation
1. Setup your environement
```
# Linux
python  -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# 🎉 You're ready
```

## Services:

_Remember to activate your virtual environment before trying to run any of the following services_
```
source .venv/bin/activate
```
### 💻 Application 
Deploy locally a `Streamlit` application enabling to interact with the pipeline and explore validation results.
```cmake
make app
```
### 📄 Documents vectorization
#### Local
Create embeddings based on the telegram conversations export. The resulting document store is stored locally in a pickle file
```cmake
make local_document_store
```

#### Pinecone DB
Create embeddings and store them in a remote [Pinecone](https://www.pinecone.io/) database.
```cmake
make pinecone
```

### 🧪 Validations
#### Last 30 questions
Run the pipeline on the validation set (aka 30 last questions asked by the model. _cf. data management section below_). Results a stored in `data/validation` folder with a name `validation_<timestamp>.json`
```cmake
make validation
```
#### Cherry picked questions
Run the pipeline on a set of cherry picked questions. Results a stored in `data/validation` folder with a name `base_de_test_validation_<timestamp>.xlsx`

```cmake
make cherry_validation
```

### ⌨ Development
#### Linters
Run `black` and `isort` code enhancer program.
```cmake
make lint
```
#### Linters
Run the unit tests
```cmake
make unit_test
```

## Data management
Most of the historical data is used to answer questions.   
The last part of the dataset is used for validation purpose (i.e. not included in the document store) and therefore not accessible for answer generation



