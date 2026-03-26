import sys
import os

# ==============================
# PATH SETUP (FIX IMPORT ISSUE)
# ==============================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LLM_PATH = os.path.join(CURRENT_DIR, "..", "01_llm_api")
sys.path.append(os.path.abspath(LLM_PATH))

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from llm_client import ask_llm, create_client

# ==============================
# CONFIG
# ==============================
PDF_PATH = os.path.join(CURRENT_DIR, "..", "02_data", "01_test.pdf")
DB_DIR = os.path.join(CURRENT_DIR, "db")
LLM_URL = "http://192.168.37.145:8000/v1"
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# ==============================
# STEP 1: LOAD PDF
# ==============================
print("STEP 1: Loading PDF...")

if not os.path.exists(PDF_PATH):
    raise FileNotFoundError(f"PDF not found at: {PDF_PATH}")

loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

print(f" Loaded {len(docs)} pages")

# ==============================
# STEP 2: EMBEDDINGS
# ==============================
print("STEP 2: Loading embeddings model...")

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print(" Embeddings ready")

# ==============================
# STEP 3: VECTOR DB (PERSISTENT)
# ==============================
print("STEP 3: Initializing vector DB...")

if os.path.exists(DB_DIR):
    print(" Loading existing DB...")
    db = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embedding
    )
else:
    print(" Creating new DB (first run, may take time)...")
    db = Chroma.from_documents(
        docs,
        embedding,
        persist_directory=DB_DIR
    )
    db.persist()

print(" Vector DB ready")

# ==============================
# STEP 4: USER INPUT LOOP
# ==============================
print("\nRAG SYSTEM READY (type 'exit' to quit)\n")

client = create_client(LLM_URL)

while True:
    try:
        query = input("Enter your question: ").strip()

        if query.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        if not query:
            continue

        # ==============================
        # STEP 5: RETRIEVAL
        # ==============================
        print("Searching relevant context...")
        results = db.similarity_search(query, k=2)

        context = "\n\n".join([doc.page_content for doc in results])

        # ==============================
        # STEP 6: PROMPT
        # ==============================
        prompt = f"""
            You are an assistant that answers ONLY using the provided context.

            Context:
            {context}

            Question:
            {query}
            """

        # ==============================
        # STEP 7: LLM CALL
        # ==============================
        print("Asking LLM...")
        answer = ask_llm(client, MODEL_NAME, prompt)

        # ==============================
        # OUTPUT
        # ==============================
        print("\n Answer:\n")
        print(answer)
        print("\n" + "="*50 + "\n")

    except KeyboardInterrupt:
        print("\n Interrupted. Exiting...")
        break

    except Exception as e:
        print(f" Error: {e}")