from langchain_community.document_loaders import DirectoryLoader,TextLoader
from pathlib import Path

def load_file(repo_path:str):
    loader=DirectoryLoader(
        repo_path,
        # glob(global) - used for pattern matching like (**/ -> check all files no matter hoqw deep)
        # *.py -> check for the files with extension py
        glob=['**/*.md','**/*.txt','**/*.java','**/*.py','**/*.html','**/*.js','**/*.xml','**/*.yml','**/*.gradle','**/.jar','**/*.properties'],
        loader_cls=TextLoader, 
        recursive=True
    )
    docs=loader.load()  # list of document obj
    for doc in docs:
        source=Path(doc.metadata['source'])
        'return the actual folder inside the main folder'
        doc.metadata['source']=str(source.relative_to(repo_path))    
    return docs
