import os
from dotenv import load_dotenv
import glob
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from PyPDF2 import PdfReader

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

NOTES_DIRECTORY = "Notes"
SUBFOLDERS = ["Lecture", "Readings", "Textbook"]
TOPICS = ['OS', 'Memory', 'Processes', 'Threads']


def get_pdf_text(pdf_docs) -> str:
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text: str) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks, store_name):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(store_name)


def generate_individual_embeddings():
    if not os.path.exists(NOTES_DIRECTORY):
        print(f"The directory {NOTES_DIRECTORY} does not exist.")
        return

    for topic in TOPICS:
        all_topic_docs = []
        for subfolder in SUBFOLDERS:
            subfolder_path = os.path.join(NOTES_DIRECTORY, subfolder, topic)
            print(f"Searching in: {subfolder_path}")
            topic_docs = glob.glob(os.path.join(subfolder_path, "*.pdf"))
            all_topic_docs.extend(topic_docs)

        if all_topic_docs:
            print(f"Generating embeddings for topic: {topic}")
            raw_text = get_pdf_text(all_topic_docs)
            text_chunks = get_text_chunks(raw_text)
            embeddings_path = f"embeddings/{topic}"
            os.makedirs(embeddings_path, exist_ok=True)
            get_vector_store(text_chunks, embeddings_path)
        else:
            print(f"No PDF documents found for topic: {topic}.")


def generate_combined_embeddings():
    all_text_chunks = []
    if not os.path.exists(NOTES_DIRECTORY):
        print(f"The directory {NOTES_DIRECTORY} does not exist.")
        return

    for subfolder in SUBFOLDERS:
        subfolder_path = os.path.join(NOTES_DIRECTORY, subfolder)
        for topic in TOPICS:
            topic_path = os.path.join(subfolder_path, topic)
            pdf_docs = glob.glob(os.path.join(topic_path, "*.pdf"))

            if pdf_docs:
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                all_text_chunks.extend(text_chunks)

    if all_text_chunks:
        combined_embeddings_path = "embeddings/All"
        os.makedirs(combined_embeddings_path, exist_ok=True)
        get_vector_store(all_text_chunks, combined_embeddings_path)
        print("Finished generating all embeddings")
    else:
        print("No PDF documents found in any subfolders.")


generate_individual_embeddings()
generate_combined_embeddings()
