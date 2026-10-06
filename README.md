# 🤖 AI Software Engineering Agent

An intelligent, conversational RAG based AI agent that lets you **chat with any GitHub repository**. Point it at a public GitHub repo, and it will clone it, index the codebase into a vector store, and give you a powerful assistant that can answer questions about the code, search the web for related context, and read any file on demand.

Built with **LangGraph**, **LangChain**, **Groq**, **ChromaDB**, and **Streamlit**.

---

## ✨ Features

- 🔗 **GitHub Repository Ingestion** — Provide any public GitHub `.git` URL and the agent clones it automatically.
- 📄 **Multi-format File Loading** — Indexes Python, Java, JavaScript, Markdown, HTML, YAML, XML, properties files, and more.
- 🧠 **Semantic Search (RAG)** — Uses `sentence-transformers/all-MiniLM-L6-v2` embeddings + ChromaDB for lightning-fast similarity search over the codebase.
- 🛠️ **Agentic Tools** — The agent has three tools at its disposal:
  - `get_context` — Semantic search over the indexed repository.
  - `get_file` — Read any specific file from the repo by path.
  - `srch_web` — Google Serper web search for external knowledge.
- 💬 **Conversational Memory** — Built with LangGraph's `InMemorySaver` for multi-turn, stateful conversations.
- 🖥️ **Streamlit UI** — Clean, interactive chat interface that runs locally in your browser.

---

## 🏗️ Project Structure

```
AISoftwareEngineeringBot/
├── app/
│   ├── main.py                  # Streamlit app entry point
│   ├── agent/
│   │   ├── agents.py            # LangGraph agent creation
│   │   └── tools.py             # Agent tools (RAG, file reader, web search)
│   ├── ingestion/
│   │   ├── github.py            # Git repository cloning
│   │   ├── file_loader.py       # Multi-format document loader
│   │   └── chunker.py           # Text splitting / chunking
│   └── retrieval/
│       └── vector_store.py      # ChromaDB vector store setup
├── workspace/
│   └── repositories/            # Cloned repos are stored here
├── env.example                  # Environment variable template
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone this repository

```bash
git clone https://github.com/your-username/AISoftwareEngineeringBot.git
cd AISoftwareEngineeringBot
```

### 2. Create a virtual environment

```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS / Linux
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your API keys:


Open `.env` and set your keys (see [Environment Variables](#-environment-variables) below).

### 5. Run the app

```bash
streamlit run app/main.py
```

The app will open at `http://localhost:8501`.

---


## 🚀 How It Works

```
User provides GitHub URL
        │
        ▼
  Clone Repository  ──────────────────────► workspace/repositories/<repo-name>/
        │
        ▼
  Load Files (py, md, js, java, html, ...)
        │
        ▼
  Chunk Documents  (1000 chars / 200 overlap)
        │
        ▼
  Embed with HuggingFace MiniLM-L6-v2
        │
        ▼
  Store in ChromaDB (in-memory)
        │
        ▼
  LangGraph Agent (Groq LLM + 3 tools)
        │
        ▼
  Streamlit Chat UI  ◄──── User questions
```



## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
