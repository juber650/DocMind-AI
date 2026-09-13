from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Load PDF
loader = PyPDFLoader("data/AWS_complete_notes.pdf")
documents = loader.load()

print("Original pages:", len(documents))

# 2. Create text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# 3. Split documents
chunks = text_splitter.split_documents(documents)

print("Total chunks:", len(chunks))

# 4. Display first chunk
print("\nFirst chunk:")
print(chunks[0].page_content)

print("\nMetadata:")
print(chunks[0].metadata)