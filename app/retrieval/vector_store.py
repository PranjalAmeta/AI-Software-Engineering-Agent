from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document 

def get_vecdb(splitted_docs:list[Document],embeddings):
    vec_store=Chroma.from_documents(
        documents=splitted_docs,
        embedding=embeddings,
    )
    return vec_store