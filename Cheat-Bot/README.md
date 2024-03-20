# CS-111 Final Chat Bot
The CS 111 final is online, so I made this langchain app which acts as a search engine for the textbook, required readings, and my lecture notes.

![image](https://github.com/Marvin-Deng/CS111/assets/52214624/5514aef7-53b0-4034-90e1-3d3c6963a76f)


## Setup

1. Clone repo
```shell
git clone https://github.com/Marvin-Deng/CS111.git
cd Cheat-Bot
```

2. Create virtual environment
```shell
python -m venv venv
```

3. Install requirements
```shell
pip install -r requirements.txt
```

4. Create a `.env` file in the Cheat-Bot directory and add your [free Gemini API key](https://aistudio.google.com/app/apikey)
```shell
GOOGLE_API_KEY = ""
```

## Running

```shell
streamlit run app.py
```

## Embeddings
- Embeddings are stored in the embeddings folder. You can add or remove notes for any topic, then regenerate the embeddings to see the changes in the app.

To generate new embeddings
```shell
python generate_embeddings.py
```
