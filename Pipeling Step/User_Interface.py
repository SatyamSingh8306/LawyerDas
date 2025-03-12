#set up pdf upload functionality
import streamlit as st 
from rag_pipeline import retrieve_docs,ans_query,model
from vector_database import upload_data

upload_file =  st.file_uploader("Upload PDF",
                                type=".pdf",
                                accept_multiple_files=False)

#chatbot skelton (Question and ANswer)
user_query = st.text_area("Enter your prompt: ",height= 150,placeholder="Ask Anything...")
ask_question = st.button("Ask LawyerDas")

if ask_question:
    if upload_file:
        # upload_data(upload_file)
        st.chat_message("user").write(user_query)
        #Rag Pipeline
        retrieved_docs=retrieve_docs(user_query)
        response=ans_query(documents=retrieved_docs, model=model, query=user_query)
        st.chat_message("LawyerDas").write(response)
    else:
        st.error("Kindly upload the file")

