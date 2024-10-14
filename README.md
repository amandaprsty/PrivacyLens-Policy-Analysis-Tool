# RAG_v5

activate venv:

conda create -n . python=3.12

conda init

--> close and reopen terminal

conda activate .

conda install -c conda-forge sqlite

#install
pip install streamlit chromadb openai llama-index langchain tiktoken python-dotenv
pip install llama-index-vector-stores-chroma
pip install --upgrade llama-index
pip install --upgrade chromadb
pip install tiktoken
sudo apt update
sudo apt install sqlite3

streamlit run Home.py

update git:
git status 
