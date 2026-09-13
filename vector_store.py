from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# 1. Load PDF
loader = PyPDFLoader("data/AWS_complete_notes.pdf")
documents = loader.load()

print("Pages:", len(documents))


# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print("Chunks:", len(chunks))


# 3. Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# 4. Create vector store
vector_store = FAISS.from_documents(
    chunks,
    embeddings
)


# 5. Create retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# 6. Ask a question
query = "What is machine learning?"

results = retriever.invoke(query)


# 7. Display results
for i, result in enumerate(results):
    print("\n==========================")
    print("Result:", i + 1)
    print("==========================")

    print(result.page_content)
    print("\nMetadata:", result.metadata)