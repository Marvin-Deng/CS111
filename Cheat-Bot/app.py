import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

from src.utils import (
    get_pdf_text,
    get_text_chunks,
    get_vector_store
)

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_conversational_chain():

    prompt_template = """
    Include the title of the document where the answer was found. Answer the question as detailed as possible from the provided context, make sure to provide all the details. Don't provide the wrong answer.\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = FAISS.load_local(
        "embeddings/notes_faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True)
    st.write(response["output_text"])


def main():
    st.set_page_config("CS-111 Final Cheat Bot")
    st.header("CS-111 Chat Bot using Gemini")

    user_question = st.text_input("Ask a question about CS 111")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload additional notes as PDF Files", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")


if __name__ == "__main__":
    main()
