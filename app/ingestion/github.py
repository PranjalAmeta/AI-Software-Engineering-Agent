from git import Repo
from pathlib import Path

def clone_repo(repo_link:str,repo_name:str,base_url:str):
    path=Path(base_url)/repo_name
    path.mkdir(parents=True,exist_ok=True)
    # print('Processing...','\n')
    
    Repo.clone_from(repo_link,path)
    # print('done')
    return path

