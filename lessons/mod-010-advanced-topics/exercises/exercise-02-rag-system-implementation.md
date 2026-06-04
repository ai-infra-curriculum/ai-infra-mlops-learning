## Exercise 2: RAG System Implementation (90 minutes)

**Objective**: Build a production-ready Retrieval-Augmented Generation system with vector search, document processing, and LLM integration.

### Background

RAG systems combine:
- Document embedding and vector storage
- Semantic search with vector databases
- Context-aware LLM generation
- Document chunking and preprocessing

### Tasks

1. **Set up vector database**:
   - Install and configure ChromaDB/Weaviate
   - Create collection with embeddings
   - Implement indexing strategy
   - Set up persistence

2. **Build document processor**:
   - Implement document chunking
   - Generate embeddings
   - Store with metadata
   - Handle multiple formats

3. **Create retrieval system**:
   - Implement semantic search
   - Rank and rerank results
   - Apply filters
   - Optimize retrieval parameters

4. **Integrate with LLM**:
   - Build prompt templates
   - Combine retrieved context
   - Generate responses
   - Implement citation tracking

### Starter Code

```python
# rag_system.py
"""
Production RAG system with LangChain and ChromaDB.
"""

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import (
    PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
)
from langchain.chains import RetrievalQA
from langchain.llms import VLLM
from langchain.prompts import PromptTemplate
from typing import List, Dict, Optional, Tuple
import chromadb
from chromadb.config import Settings
import logging
from pathlib import Path
import hashlib

class DocumentProcessor:
    """
    Process and chunk documents for RAG.

    TODO: Implement document processing pipeline
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: Optional[List[str]] = None
    ):
        """
        Initialize document processor.

        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            separators: Custom separators for splitting

        TODO: Set up text splitter
        """
        # TODO: Initialize text splitter
        # self.text_splitter = RecursiveCharacterTextSplitter(
        #     chunk_size=chunk_size,
        #     chunk_overlap=chunk_overlap,
        #     separators=separators or ["\n\n", "\n", " ", ""]
        # )

        self.supported_formats = {
            '.pdf': PyPDFLoader,
            '.txt': TextLoader,
            '.md': UnstructuredMarkdownLoader
        }

    def load_document(self, file_path: str) -> List[Dict]:
        """
        Load document from file.

        TODO: Implement document loading
        - Detect file type
        - Use appropriate loader
        - Extract metadata
        """
        path = Path(file_path)

        # TODO: Check file type
        if path.suffix not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {path.suffix}")

        # TODO: Load document
        # loader_class = self.supported_formats[path.suffix]
        # loader = loader_class(file_path)
        # documents = loader.load()

        # TODO: Add metadata
        # for doc in documents:
        #     doc.metadata['source'] = file_path
        #     doc.metadata['file_type'] = path.suffix
        #     doc.metadata['doc_id'] = self._generate_doc_id(file_path)

        # return documents

        pass

    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Split documents into chunks.

        TODO: Implement chunking with metadata preservation
        """
        # TODO: Split documents
        # chunks = self.text_splitter.split_documents(documents)

        # TODO: Add chunk metadata
        # for i, chunk in enumerate(chunks):
        #     chunk.metadata['chunk_id'] = i
        #     chunk.metadata['chunk_size'] = len(chunk.page_content)

        # return chunks

        pass

    def process_directory(self, directory: str) -> List[Dict]:
        """
        Process all documents in a directory.

        TODO: Implement batch processing
        """
        all_chunks = []
        dir_path = Path(directory)

        # TODO: Process all supported files
        # for file_path in dir_path.rglob('*'):
        #     if file_path.suffix in self.supported_formats:
        #         try:
        #             docs = self.load_document(str(file_path))
        #             chunks = self.chunk_documents(docs)
        #             all_chunks.extend(chunks)
        #             logging.info(f"Processed {file_path}: {len(chunks)} chunks")
        #         except Exception as e:
        #             logging.error(f"Failed to process {file_path}: {e}")

        # return all_chunks

        pass

    @staticmethod
    def _generate_doc_id(file_path: str) -> str:
        """Generate unique document ID."""
        return hashlib.md5(file_path.encode()).hexdigest()


class RAGVectorStore:
    """
    Vector store for RAG with ChromaDB.

    TODO: Implement vector storage and retrieval
    """

    def __init__(
        self,
        collection_name: str = "rag_documents",
        persist_directory: str = "./chroma_db",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        """
        Initialize vector store.

        TODO: Set up ChromaDB and embeddings
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        # TODO: Initialize embeddings
        # self.embeddings = HuggingFaceEmbeddings(
        #     model_name=embedding_model,
        #     model_kwargs={'device': 'cuda'},  # or 'cpu'
        #     encode_kwargs={'normalize_embeddings': True}
        # )

        # TODO: Initialize ChromaDB client
        # self.chroma_client = chromadb.Client(
        #     Settings(
        #         chroma_db_impl="duckdb+parquet",
        #         persist_directory=persist_directory
        #     )
        # )

        # TODO: Create or get collection
        # self.vectorstore = Chroma(
        #     collection_name=collection_name,
        #     embedding_function=self.embeddings,
        #     persist_directory=persist_directory
        # )

    def add_documents(self, documents: List[Dict], batch_size: int = 100):
        """
        Add documents to vector store.

        TODO: Implement batch insertion
        - Process in batches
        - Handle duplicates
        - Update existing documents
        """
        # TODO: Process in batches
        # for i in range(0, len(documents), batch_size):
        #     batch = documents[i:i+batch_size]
        #
        #     try:
        #         self.vectorstore.add_documents(batch)
        #         logging.info(f"Added batch {i//batch_size + 1}: {len(batch)} documents")
        #     except Exception as e:
        #         logging.error(f"Failed to add batch: {e}")

        # TODO: Persist changes
        # self.vectorstore.persist()

        pass

    def search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict] = None,
        score_threshold: Optional[float] = None
    ) -> List[Tuple[Dict, float]]:
        """
        Search for relevant documents.

        TODO: Implement semantic search with filtering
        """
        # TODO: Perform similarity search
        # if score_threshold:
        #     results = self.vectorstore.similarity_search_with_relevance_scores(
        #         query,
        #         k=k,
        #         filter=filter,
        #         score_threshold=score_threshold
        #     )
        # else:
        #     docs = self.vectorstore.similarity_search(
        #         query,
        #         k=k,
        #         filter=filter
        #     )
        #     results = [(doc, 1.0) for doc in docs]

        # return results

        pass

    def get_retriever(self, **kwargs):
        """
        Get retriever for LangChain integration.

        TODO: Create retriever with search parameters
        """
        # return self.vectorstore.as_retriever(
        #     search_kwargs=kwargs
        # )
        pass


class RAGPipeline:
    """
    End-to-end RAG pipeline.

    TODO: Implement complete RAG system
    """

    def __init__(
        self,
        vectorstore: RAGVectorStore,
        llm_endpoint: str = "http://localhost:8000",
        model_name: str = "meta-llama/Llama-2-7b-chat-hf"
    ):
        """
        Initialize RAG pipeline.

        TODO: Set up LLM and retrieval chain
        """
        self.vectorstore = vectorstore

        # TODO: Initialize LLM
        # self.llm = VLLM(
        #     endpoint_url=f"{llm_endpoint}/v1/completions",
        #     model_name=model_name,
        #     temperature=0.7,
        #     max_tokens=512
        # )

        # TODO: Create prompt template
        self.prompt_template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Always cite the source of your information using [Source: filename].

Context:
{context}

Question: {question}

Answer: """

        # TODO: Create prompt
        # self.prompt = PromptTemplate(
        #     template=self.prompt_template,
        #     input_variables=["context", "question"]
        # )

    def query(
        self,
        question: str,
        k: int = 4,
        return_sources: bool = True
    ) -> Dict:
        """
        Query the RAG system.

        TODO: Implement retrieval and generation
        - Retrieve relevant documents
        - Format context
        - Generate answer
        - Return with sources
        """
        # TODO: Retrieve documents
        # retriever = self.vectorstore.get_retriever(k=k)

        # TODO: Create RetrievalQA chain
        # qa_chain = RetrievalQA.from_chain_type(
        #     llm=self.llm,
        #     chain_type="stuff",
        #     retriever=retriever,
        #     return_source_documents=return_sources,
        #     chain_type_kwargs={"prompt": self.prompt}
        # )

        # TODO: Generate answer
        # result = qa_chain({"query": question})

        # TODO: Format response
        # response = {
        #     "answer": result["result"],
        #     "question": question
        # }

        # if return_sources:
        #     response["sources"] = [
        #         {
        #             "content": doc.page_content,
        #             "metadata": doc.metadata
        #         }
        #         for doc in result["source_documents"]
        #     ]

        # return response

        pass

    def batch_query(self, questions: List[str]) -> List[Dict]:
        """
        Process multiple queries.

        TODO: Implement batch processing
        """
        # return [self.query(q) for q in questions]
        pass


# Example usage
if __name__ == "__main__":
    # TODO: Initialize components
    # processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)

    # TODO: Process documents
    # chunks = processor.process_directory("./documents")
    # print(f"Processed {len(chunks)} chunks")

    # TODO: Initialize vector store
    # vectorstore = RAGVectorStore(
    #     collection_name="my_documents",
    #     persist_directory="./chroma_db"
    # )

    # TODO: Add documents
    # vectorstore.add_documents(chunks)

    # TODO: Initialize RAG pipeline
    # rag = RAGPipeline(vectorstore=vectorstore)

    # TODO: Query
    # response = rag.query("What is machine learning?")
    # print(response)

    pass
```

### Success Criteria

- [ ] Documents are chunked appropriately
- [ ] Embeddings are generated correctly
- [ ] Vector search returns relevant results
- [ ] LLM generates accurate answers with citations
- [ ] System handles multiple document formats
- [ ] Retrieval latency is under 500ms
- [ ] Generated answers are factually grounded

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Chunking**: Use recursive splitter with overlap for context preservation
2. **Embeddings**: Use sentence-transformers models for efficiency
3. **Vector DB**: ChromaDB for local, Pinecone/Weaviate for production
4. **Retrieval**: Use MMR (Maximal Marginal Relevance) for diversity
5. **Prompting**: Include clear instructions and examples in template
6. **Citations**: Track source metadata through the pipeline

</details>

---
