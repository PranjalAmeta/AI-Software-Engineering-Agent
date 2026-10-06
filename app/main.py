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

load_dotenv()

'''
CREATE CHAIN AT END 
'''

### UI
st.title('🤖 AI Software Engineering Agent 🤖')


## Make the execution stop till we dont get the link
if 'link_uploaded' not in st.session_state:
    st.session_state.link_uploaded=False

## Session state should have memory and link and agent
if 'messages' not in st.session_state:
    st.session_state.messages=[]

if 'agent' not in st.session_state:
    st.session_state.agent=None

    
base_url=Path(__file__).resolve().parents[1]
path=base_url/'workspace'/'repositories'

## cloning 
def process_docs(repo_link:str,path:str):

    def clone_repositories(repo_link:str,path:str):
        repo_name=repo_link.split('/')[-1].removesuffix('.git')
        new_path=path/repo_name
        if(new_path.exists()):
            return new_path
        return clone_repo(repo_link,repo_name,path)


    repo_path=clone_repositories(repo_link,path)
    # print(repo_path)

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

    st.session_state.agent=agent
    st.session_state.link_uploaded=True


        

if not st.session_state.link_uploaded:
    repo_link=st.text_input('Enter the repository link: ')
    if(not repo_link.endswith('.git')):
        print('Enter a correct github link')
    else:
        with st.spinner('Processing...'):
            process_docs(repo_link,path)
        st.rerun()

if st.session_state.link_uploaded and st.session_state.agent:

    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content']) 

    query=st.chat_input('Enter your Query...')
    if query:
        st.chat_message('user').markdown(query)
        st.session_state.messages.append({'role':'user','content':query})
        res=res=st.session_state.agent.invoke(
            {'messages':[
                {'role':'user','content':query},
            ]},
            config={'configurable':{'thread_id':1},'recursion_limit':10},
        )
        ans=res['messages'][-1].content 
        st.session_state.messages.append({'role':'ai','content':ans})
        st.chat_message('ai').markdown(ans)