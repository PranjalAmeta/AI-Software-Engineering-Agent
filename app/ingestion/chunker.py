from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_docs(docs):
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    splitted_docs=splitter.split_documents(docs)
    return splitted_docs