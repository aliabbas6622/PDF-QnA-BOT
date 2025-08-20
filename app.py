
import os
import sys
import asyncio

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate


# Load API key from .env
load_dotenv()

# Initialize LLM (auto uses GOOGLE_API_KEY from env)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

# Prompt template
prompt = PromptTemplate(
    template="You are an ai assistant. This is the text retrieved from the document:\n{docs}\n read the text \nAnd this is the query which a  user asked about the document: {query}",
    input_variables=["docs", "query"]
)

# Streamlit UI
st.set_page_config(page_title="📄 PDF QnA with Gemini", layout="wide")
st.title("📄 Ask Questions from your PDF")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    # Save uploaded PDF temporarily
    pdf_path = f"temp_{uploaded_file.name}"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ PDF uploaded successfully!")

    # Load PDF
    st.success("Processing Pdf")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # Create vector store
    vector_store = Chroma(
        collection_name="pdf_data",
        embedding_function=GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        ),
        persist_directory="./chroma_db"
    )

    # Add documents
    vector_store.add_documents(docs)

    # Input box for query
    query = st.text_input("Ask a question about your PDF:")

    if query:
        with st.spinner("Thinking... 🤔"):
            retrieved_docs = vector_store.similarity_search(query, k=3)
            retrieved_text = ""
            for doc in retrieved_docs:
                retrieved_text += doc.page_content + "\n"

            result = llm.invoke(
                prompt.format(docs=retrieved_text, query=query)
            )

        st.subheader("Answer:")
        st.write(result.content)
