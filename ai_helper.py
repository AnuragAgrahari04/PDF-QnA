import os
from typing import Optional
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
from langchain_community.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

load_dotenv()  # Optional if you want to use .env file

class PDFQuestionAnswerer:
    def __init__(self, embedding_model="embed-english-v3.0", llm_model="command"):
        # Load API key from Streamlit secrets
        self.api_key = st.secrets["COHERE_API_KEY"]

        # Setup embeddings
        self.embeds = CohereEmbeddings(
            cohere_api_key=self.api_key,
            model=embedding_model
        )

        # Setup LLM
        self.llm = Cohere(
            model=llm_model,
            temperature=0.3,
            cohere_api_key=self.api_key
        )

        # State
        self.docsearch = None
        self.chain = None
        self.current_pdf_path: Optional[str] = None

    def load_and_process_pdf(self, pdf_path: str, chunk_size=500, chunk_overlap=50):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Load and split PDF
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_documents(documents)

        # Embed and index
        self.docsearch = FAISS.from_documents(chunks, self.embeds)

        # Create RAG chain
        retriever = self.docsearch.as_retriever()
        retriever_pipe = RunnableParallel({
            "context": retriever,
            "question": RunnablePassthrough()
        })

        prompt_template = """
Text: {context}
Question: {question}

Answer the question based only on the text above. If you don’t know the answer, say "Not found in document".
"""
        prompt = PromptTemplate.from_template(prompt_template)

        self.chain = retriever_pipe | prompt | self.llm | StrOutputParser()
        self.current_pdf_path = pdf_path

        return len(chunks)

    def ask_question(self, question: str) -> str:
        if not self.chain:
            raise ValueError("PDF not loaded yet.")
        return self.chain.invoke(question)
