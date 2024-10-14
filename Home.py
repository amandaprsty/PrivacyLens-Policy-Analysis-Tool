import streamlit as st
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
import sys
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.indices.prompt_helper import PromptHelper
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import download_loader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from openai import OpenAI as OpenAIClient
import os
import tempfile

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import chromadb
except ImportError:
    st.write("Installing chromadb...")
    install_package('chromadb')
    import chromadb

# Load environment variables
load_dotenv()

# Set up OpenAI client
openai_client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))

# Set up Streamlit page
st.set_page_config(page_title="PrivacyLens: Policy Analysis Tool")
st.title("PrivacyLens: Policy Analysis Tool")

# Initialize Chroma client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create or get existing collection for storing document embeddings
collection_name = "document_collection"
try:
    chroma_collection = chroma_client.get_collection(name=collection_name)
except ValueError:
    chroma_collection = chroma_client.create_collection(name=collection_name)

# Set up LlamaIndex components
llm = OpenAI(model="gpt-4o-mini", temperature=0.1)
embed_model = OpenAIEmbedding()
prompt_helper = PromptHelper(
    context_window=4096,
    num_output=256,
    chunk_overlap_ratio=0.1,
    chunk_size_limit=None
)

# Function to process uploaded file
def process_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name

    if uploaded_file.type == "application/pdf":
        PDFReader = download_loader("PDFReader")
        loader = PDFReader()
        documents = loader.load_data(file=temp_file_path)
    else:
        documents = SimpleDirectoryReader(input_files=[temp_file_path]).load_data()
    
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
        prompt_helper=prompt_helper
    )

    os.unlink(temp_file_path)
    return index

# Streamlit UI
uploaded_file = st.file_uploader("Choose a file :memo:", type=["txt", "pdf"])

if uploaded_file is not None:
    index = process_file(uploaded_file)
    st.success("Document processed successfully!")
    query = st.text_input("Ask a question about the Privacy Policy document:")
    if query:
        query_engine = index.as_query_engine(llm=llm)
        response = query_engine.query(query)
    if query:
        if st.button("Get Answer"):
            st.write("Answer:", response.response)
else:
    st.write("Please upload a document to get started.")

# UI IMPROVEMENT: Sidebar
# Fixed: Added indentation to the code block under 'with st.sidebar:'
with st.sidebar:  
    st.title("PrivacyLens: Policy Analysis Tool")
    st.markdown("---")
    st.markdown("""
    PrivacyLens is an AI-powered tool designed to help you understand and navigate complex privacy policies with ease.

    ### :pushpin: Key Features
    - Upload and analyse privacy policy documents
    - Ask questions in plain language
    - Get concise, relevant answers

    ### :pushpin: How to Use
    1. Upload a privacy policy document (PDF or TXT)
    2. Wait for the document to be processed
    3. Ask questions about the policy in the text box
    4. Receive AI-generated answers based on the document content

    PrivacyLens makes policy analysis quick, easy, and accessible. Start exploring your privacy policies today! :mag:
    """)
    st.markdown("---")

##OPENAPI KEY
if "OPENAI_API_KEY" not in st.session_state:
    st.session_state.openai_api_key = None

def render_sidebar():
    st.sidebar.title("API Key Input")
    api_key = st.sidebar.text_input("Enter your API key:")
    update_button = st.sidebar.button("Update API Key")
    return api_key, update_button

api_key, update_button = render_sidebar()

if update_button:
    st.session_state.openai_api_key = api_key

# UI IMPROVEMENT: Footer
st.markdown("---")
st.markdown("© 2024 AP Company. All rights reserved.")