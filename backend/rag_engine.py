import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class RAGEngine:
    """RAG implementation with intentional vulnerabilities"""
    
    def __init__(self):
        self.db_path = "./data/vector_db"
        self.knowledge_base_path = "./data/knowledge_base"
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Use default embedding function (vulnerable - no access control)
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="dealership_knowledge",
            embedding_function=self.embedding_function
        )
        
        self.initialized = False
        
    def load_documents(self):
        """Load all documents from knowledge base - no filtering"""
        documents = []
        metadatas = []
        ids = []
        
        knowledge_path = Path(self.knowledge_base_path)
        if not knowledge_path.exists():
            logger.warning(f"Knowledge base path {knowledge_path} does not exist")
            return
        
        # Load all files indiscriminately (vulnerability: includes sensitive docs)
        for file_path in knowledge_path.glob("*.txt"):
            with open(file_path, 'r') as f:
                content = f.read()
                
                # Split into chunks (simple splitting - another vulnerability)
                chunks = self._simple_chunk(content, chunk_size=500)
                
                for i, chunk in enumerate(chunks):
                    documents.append(chunk)
                    metadatas.append({
                        "source": file_path.name,
                        "chunk_id": i,
                        # Vulnerability: expose file classification
                        "is_confidential": "confidential" in file_path.name.lower()
                    })
                    ids.append(f"{file_path.name}_{i}")
        
        # Add to collection if we have documents
        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Loaded {len(documents)} document chunks")
            self.initialized = True
    
    def _simple_chunk(self, text: str, chunk_size: int = 500) -> List[str]:
        """Simple chunking - vulnerable to context manipulation"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            current_chunk.append(word)
            current_size += len(word) + 1
            
            if current_size >= chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def get_context(self, query: str, n_results: int = 3) -> str:
        """Retrieve context - vulnerable to injection and leakage"""
        try:
            # Query collection (no sanitization of query)
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Build context string (vulnerable concatenation)
            context_parts = []
            
            if results['documents'] and results['documents'][0]:
                for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                    # Vulnerability: Include metadata in context
                    source = metadata.get('source', 'unknown')
                    is_confidential = metadata.get('is_confidential', False)
                    
                    # Add document with metadata (leaks information structure)
                    context_parts.append(
                        f"[Source: {source}] [Confidential: {is_confidential}]\n{doc}"
                    )
            
            context = "\n\n---\n\n".join(context_parts)
            
            # Log retrieved context (another vulnerability)
            logger.info(f"Retrieved context for query: {query[:50]}...")
            
            return context
            
        except Exception as e:
            logger.error(f"RAG retrieval error: {str(e)}")
            return ""
    
    def is_initialized(self) -> bool:
        """Check if RAG is initialized with documents"""
        return self.initialized
    
    def reset_collection(self):
        """Clear and reset the collection"""
        try:
            self.client.delete_collection("dealership_knowledge")
            self.collection = self.client.create_collection(
                name="dealership_knowledge",
                embedding_function=self.embedding_function
            )
            self.initialized = False
            logger.info("Collection reset")
        except Exception as e:
            logger.error(f"Error resetting collection: {str(e)}")