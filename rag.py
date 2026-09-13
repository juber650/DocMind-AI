from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


# ==========================================
# 1. Create Embeddings
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==========================================
# 2. Create Prompt
# ==========================================

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful AI assistant.

Answer the question using ONLY the information
provided in the context.

If the answer is not available in the context,
say:

\"I don't know based on the provided document.\"

Context:
{context}

Question:
{question}
"""
)


# ==========================================
# 3. Create Local Ollama LLM
# ==========================================

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


# ==========================================
# 4. Retriever
# ==========================================

retriever = None


# ==========================================
# 5. Function to Create RAG from PDF
# ==========================================

def create_rag_from_pdf(pdf_path):

    global retriever

    print("\n==========================================")
    print("Loading PDF:", pdf_path)
    print("==========================================")


    # ==========================================
    # Load PDF
    # ==========================================

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    print("Pages loaded:", len(documents))


    # ==========================================
    # Split PDF into chunks
    # ==========================================

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    print("Chunks created:", len(chunks))


    # ==========================================
    # Create FAISS Vector Store
    # ==========================================

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    print("Vector store created!")


    # ==========================================
    # Create Retriever
    # ==========================================

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    print("Retriever updated!")

    print("==========================================")
    print("RAG is ready!")
    print("==========================================")

    return len(documents), len(chunks)

