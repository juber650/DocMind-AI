from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple language."
)

llm = ChatOpenAI(
    model="gpt-4o-mini"
)

chain = prompt | llm

response = chain.invoke({
    "topic": "RAG"
})

print(response.content)