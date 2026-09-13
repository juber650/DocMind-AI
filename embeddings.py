from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

text = "Machine learning is a branch of artificial intelligence."

vector = embeddings.embed_query(text)

print("Vector length:", len(vector))
print("First 10 numbers:", vector[:10])