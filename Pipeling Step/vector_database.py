from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader,PyMuPDFLoader,PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings

pdf_directory = "pdfs/"


#upload and load the raw PDF
def upload_data(file):
    with open(pdf_directory + file.name,"wb") as f:
        f.write(file.getbuffer())
    

def load_data(path):
    # loader = DirectoryLoader(
    #     path = path,
    #     glob = "*.pdf",
    #     loader_cls=PyMuPDFLoader
    # )
    loader = PDFPlumberLoader(file_path=path)
    return loader.load()

#create chunks
def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        add_start_index = True
    )
    chunks = splitter.split_documents(documents)
    return chunks


#set up embedding model (USe Deepseek R1 with Ollama)
ollama_model_name = "deepseek-r1:1.5b"

def get_embedding_model(model_name):
    embedding_model = OllamaEmbeddings(
        model = model_name
    )
    return embedding_model

#Pipeling
file_path = "pdfs/eng.pdf"
documents = load_data(file_path)
chunks = create_chunks(documents)
embedding_model = get_embedding_model(ollama_model_name)

#index documnets ** store the chunks data in FAISS vector store **
DB_PATH = "vectorstore/db_faiss"
db = FAISS.from_documents(chunks,embedding_model)
db.save_local(DB_PATH)
