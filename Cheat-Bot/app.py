import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

TOPICS = ["All"]
TOPICS.extend(os.listdir(r"Notes\Textbook"))


def get_conversational_chain(question_type):
    if question_type == "Single Select":
        question_type_prompt = "This question has only one correct answer."
    else:
        question_type_prompt = "This question may have multiple correct answers. Provide answers in an ordered list"

    prompt_template = f"""
    Read the instructions in the question carefully and correctly answer the question. 
    {question_type_prompt}
    Some questions only have one answer and others may have multiple. 
    Don't provide the wrong answer. 
    Only pick answers that correctly answer the question.\n\n
    Context:\n{{context}}?\n
    Question: \n{{question}}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def load_faiss_index_by_topic(topic: str):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    index_path = "embeddings/All" if topic == 'All' else f"embeddings/{topic}"

    if not os.path.exists(index_path):
        st.write(f"No embeddings found for the topic '{topic}'.")
        return None

    faiss_index = FAISS.load_local(
        index_path, embeddings, allow_dangerous_deserialization=True)
    return faiss_index


def user_input(user_question, topic, question_type):
    new_db = load_faiss_index_by_topic(topic)
    
    if new_db is None:
        st.write(
            "No relevant database found. Please try a different topic or upload more documents.")
        return

    docs = new_db.similarity_search(user_question)

    try:
        chain = get_conversational_chain(question_type)
        response = chain(
            {"input_documents": docs, "question": user_question}, return_only_outputs=True)
        st.write(response["output_text"])
    except Exception:
        st.write("The model stopped generating text unexpectedly. Please try again with a different query or adjust the prompt.")


def main():
    st.set_page_config("CS-111 Final Cheat Bot")
    st.header("CS-111 Chat Bot using Gemini")

    topic = st.sidebar.selectbox('Choose a topic', TOPICS)
    question_type = st.sidebar.radio("Question Type", ["Single Select", "Multi-Select"])

    user_question = st.text_input("Ask a question about CS 111")

    if user_question:
        user_input(user_question, topic, question_type)

if __name__ == "__main__":
    main()
