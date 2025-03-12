from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from vector_database import db
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY") 

#Set up llm using groq
model = ChatGroq(
    model = "deepseek-r1-distill-llama-70b"
)

#retrive docs
def retrieve_docs(query):
    document = db.similarity_search(query)
    return document

def get_context(documents):
    if not documents:
        return "No Relevent Information found!"
    context = "\n\n".join((doc.page_content for doc in documents))
    return context


#answer question
custom_prompt_template = """
Use the pieces of information provided in the context to answer user's question.
If you dont know the answer, just say that you dont know, dont try to make up an answer. 
Dont provide anything out of the given context
Question: {question} 
Context: {context} 
Answer:
"""

def ans_query(documents,model,query):
    context = get_context(documents)
    prompt = ChatPromptTemplate.from_template(
        template=custom_prompt_template
        # input = ["context","question"]
    )
    chain = prompt | model
    ans = chain.invoke({"question":query,"context":context})
    return ans 


