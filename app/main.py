from pydantic_core._pydantic_core import _recursion_limit
from pathlib import Path
from dotenv import load_dotenv
from ingestion.github import clone_repo
from ingestion.file_loader import load_file
from ingestion.chunker import split_docs   
from retrieval.vector_store import get_vecdb
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from agent.agents import create_assistant
import streamlit as st


# st.title('AI Software Engineering Assistant')
# repo_link=st.text_input('Enter the repo file')

load_dotenv()

'''
CREATE CHAIN AT END 
'''

base_url=Path(__file__).resolve().parents[1]
path=base_url/'workspace'/'repositories'

## cloning 
def clone_repositories(repo_link:str,path:str):
    if(repo_link.endswith('.git')):
        repo_name=repo_link.split('/')[-1].removesuffix('.git')
        new_path=path/repo_name
        if(new_path.exists()):
            return new_path
        return clone_repo(repo_link,repo_name,path)

    

    

repo_path=clone_repositories("https://github.com/Naman5981/Employee-Performance-Tracker.git",path)
        

# ## getting chunks
docs=load_file(repo_path)     ## Will have list of document with each que
# print(docs[0].metadata['source'])

 

# ## Getting chunks
splitted_docs=split_docs(docs)
# print(splitted_docs)


## embeddings
embeddings=HuggingFaceEmbeddings(
    model='sentence-transformers/all-MiniLM-L6-v2'
)

### vector db
vector_stores=get_vecdb(splitted_docs,embeddings)
# print(vector_stores)
# print(vector_stores.similarity_search("trie"))



system_prompt='''
    - You are a helpful assistant that will be used to help in understanding the workflow of projects
      and anything related to it .
    - if you got any question outside the given project than you can also search for it.
'''

llm=ChatGroq(
    model='openai/gpt-oss-120b'
)

agent=create_assistant(llm,system_prompt,vector_stores,repo_path)

res=agent.invoke({
    'messages':[
        {'role':'user','content':'what is the entry point and how does controller works'}
    ],
    'recursion_limit':10
})
print(res,"\n\n\n")
print(res['messages'][-1].content) 