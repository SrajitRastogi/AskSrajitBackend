from dotenv import load_dotenv
import os

load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from resume_loader import load_resume


# 1️⃣ Load resume text
raw_text = load_resume()

# 2️⃣ Chunk properly
splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)

documents = splitter.create_documents([raw_text])

# 3️⃣ Initialize embeddings
embeddings = OpenAIEmbeddings()

# 4️⃣ Create FAISS index
vector_store = FAISS.from_documents(documents, embeddings)
