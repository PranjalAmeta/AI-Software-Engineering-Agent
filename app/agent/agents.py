
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from agent.tools import create_tools


def create_assistant(llm,system_prompt,vector_stores,repo_path):
    tools=create_tools(repo_path,vector_stores)
    agent=create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )
    return agent

