from langchain.tools import tool
from pathlib import Path
from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper


def create_tools(repo_path:str,vector_stores)->list:
    """
        - This function will be used to create tools for the given file path
    """

    @tool
    def get_context(query:str):
        """
        Search the current GitHub repository for relevant code and documentation.

        Use this FIRST when the user asks about files, classes, functions,
        algorithms, implementation details, or anything that may exist
        inside the current repository.

        This tool returns relevant code along with the file path.
        """
        docs=vector_stores.similarity_search(query,k=5)
        context=''
        for doc in docs:
            context+=(f'file:{doc.metadata["source"]}'\
                    f'\n{doc.page_content}\n'
                    )
        return context

    @tool
    def get_file(file_path:str):
        '''
        If you get the correct file path use this also and
        read the complete file for the repository
        ''' 

        full_path=(repo_path/file_path).resolve()

        if not full_path.is_relative_to(repo_path):  ### checks if the file is inside the repo folder
            return "Invalid file path"
        
        if not full_path.is_file():
            return 'file not found'

        return full_path.read_text(encoding="utf-8")
    
    srch=GoogleSerperAPIWrapper()

    @tool 
    def srch_web(query:str):
        '''
            - thius tool will be used to gain extra functionality and knowldge about the repository
             and how it works
        '''
        return srch.run(query)

    return [get_context,get_file,srch_web]