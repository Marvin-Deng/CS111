# CS-111 Final Chat Bot
The CS 111 final is online, so I made this langchain app which acts as a search engine for the textbook, required readings, and my lecture notes.

## Setup

1. Clone repo
```shell
git clone https://github.com/Marvin-Deng/CS111.git
```

2. Enter directory
```shell
cd Cheat-Bot
```

4. Create virtual environment
```shell
python -m venv venv
```

5. Install requirements
```shell
pip install -r requirements.txt
```

## Running

Running the app
```shell
streamlit run app.py
```

## Embeddings
- Embeddings are stored in the embeddings folder. You can add or remove notes for any topic, then regenerate the embeddings to see the changes in the app.

To generate new embeddings
```shell
python generate_embeddings.py
```