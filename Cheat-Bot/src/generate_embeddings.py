import os
from dotenv import load_dotenv
import glob
import google.generativeai as genai

from utils import (
    get_pdf_text,
    get_text_chunks,
    get_vector_store
)

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

NOTES_DIRECTORY =  "Notes"
SUBFOLDERS = ["Midterm 1", "Readings", "Textbook"]


def generate_embeddings():
    pdf_docs = []

    if not os.path.exists(NOTES_DIRECTORY):
        print(f"The directory {NOTES_DIRECTORY} does not exist.")
        return
    
    for subfolder in SUBFOLDERS:
        subfolder_path = os.path.join(NOTES_DIRECTORY, subfolder)
        print(subfolder_path)
        pdf_docs.extend(glob.glob(os.path.join(subfolder_path, "*.pdf")))

    if pdf_docs:
        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks, "embeddings/notes_faiss_index")
    else:
         print("No PDF documents found in the specified subfolders.")
        
generate_embeddings()