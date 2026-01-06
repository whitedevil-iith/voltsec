"""
RAG tools for voltsec_ai.
Provides code indexing and querying capabilities.
"""

import os
from typing import List, Optional
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from crewai.tools import BaseTool

from .config import config


class CodebaseRAGTool(BaseTool):
    """Tool for querying codebase using RAG (Retrieval Augmented Generation)."""
    
    name: str = "codebase_query"
    description: str = (
        "Query the indexed codebase to retrieve relevant code snippets. "
        "Input should be a search query describing what code you're looking for."
    )
    
    def __init__(self, repo_path: str):
        """
        Initialize the RAG tool with a repository path.
        
        Args:
            repo_path: Path to the repository to index
        """
        super().__init__()
        self.repo_path = repo_path
        self.vectorstore: Optional[Chroma] = None
        self._index_codebase()
    
    def _index_codebase(self) -> None:
        """Index the codebase for RAG queries."""
        print(f"Indexing codebase at: {self.repo_path}")
        
        # File extensions to include
        file_extensions = [
            ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cpp", ".c", ".h",
            ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".scala",
            ".sh", ".bash", ".yaml", ".yml", ".json", ".md"
        ]
        
        documents: List[Document] = []
        
        # Load documents from directory
        for ext in file_extensions:
            try:
                loader = DirectoryLoader(
                    self.repo_path,
                    glob=f"**/*{ext}",
                    loader_cls=TextLoader,
                    show_progress=True,
                    use_multithreading=True,
                    silent_errors=True
                )
                docs = loader.load()
                documents.extend(docs)
            except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as e:
                print(f"Warning: Error loading {ext} files: {e}")
        
        print(f"Loaded {len(documents)} documents")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        splits = text_splitter.split_documents(documents)
        print(f"Created {len(splits)} text chunks")
        
        # Create embeddings using Ollama
        embeddings = OllamaEmbeddings(
            base_url=config.ollama_base_url,
            model=config.ollama_model
        )
        
        # Create vector store with absolute path
        persist_dir = Path(self.repo_path).absolute() / ".voltsec_ai_chroma"
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=str(persist_dir)
        )
        
        print("Codebase indexing complete!")
    
    def _run(self, query: str) -> str:
        """
        Execute the tool to query the codebase.
        
        Args:
            query: Search query for relevant code
            
        Returns:
            Relevant code snippets as a string
        """
        if not self.vectorstore:
            return "Error: Vectorstore not initialized"
        
        # Retrieve relevant documents
        docs = self.vectorstore.similarity_search(query, k=5)
        
        # Format results
        results = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Unknown")
            content = doc.page_content
            results.append(f"\n--- Document {i} (from {source}) ---\n{content}\n")
        
        return "\n".join(results) if results else "No relevant code found."


def create_rag_tool(repo_path: str) -> CodebaseRAGTool:
    """
    Create a RAG tool for the specified repository.
    
    Args:
        repo_path: Path to the repository to analyze
        
    Returns:
        Initialized CodebaseRAGTool
    """
    return CodebaseRAGTool(repo_path=repo_path)
