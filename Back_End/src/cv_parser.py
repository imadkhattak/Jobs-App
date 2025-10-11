# src/CV_Parser.py

from langchain_community.document_loaders import PyPDFLoader

def extract_text(file_path):

    loader = PyPDFLoader(file_path, mode="single", pages_delimiter="\n-------THIS IS A CUSTOM END OF PAGE-------\n")
    docs = loader.load()
    text = "\n".join([doc.page_content for doc in docs])
    return text




