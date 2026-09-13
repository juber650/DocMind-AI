from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/AWS_complete_notes.pdf")

documents = loader.load()

print("Number of pages:", len(documents))

for i, document in enumerate(documents):
    print("\n--------------------")
    print("Page:", i + 1)
    print("--------------------")

    print(document.page_content[:500])
    print("Metadata:", document.metadata)