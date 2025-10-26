# Module 10: Advanced MLOps Topics - Exercises

## Overview

This exercise set provides hands-on practice with advanced MLOps techniques, including:
- LLMOps and LLM serving with vLLM
- Retrieval-Augmented Generation (RAG) systems
- Edge ML optimization and quantization
- AutoML pipeline development
- Real-time ML with feature stores

**Time Estimate**: 7.5 hours total

---

## Exercise 1: LLMOps with vLLM Serving (90 minutes)

**Objective**: Deploy and serve a large language model using vLLM with proper resource management, monitoring, and optimization.

### Background

vLLM provides:
- High-throughput LLM serving with PagedAttention
- Continuous batching for improved throughput
- Optimized CUDA kernels
- OpenAI-compatible API
- Multi-GPU support

### Tasks

1. **Set up vLLM serving infrastructure**:
   - Install vLLM with GPU support
   - Configure model serving
   - Set up resource limits
   - Implement health checks

2. **Deploy LLM with optimization**:
   - Load model with quantization
   - Configure batching parameters
   - Set up tensor parallelism (multi-GPU)
   - Implement caching strategies

3. **Create monitoring and logging**:
   - Track request latency
   - Monitor GPU utilization
   - Log token usage
   - Implement rate limiting

4. **Build production API**:
   - Create FastAPI wrapper
   - Add authentication
   - Implement request validation
   - Set up load balancing

### Starter Code

```python
# llm_serving.py
"""
vLLM-based LLM serving with production features.
"""

from vllm import LLM, SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, AsyncIterator
import asyncio
import logging
import time
from prometheus_client import Counter, Histogram, Gauge
import uvicorn

# Prometheus metrics
REQUESTS_TOTAL = Counter('llm_requests_total', 'Total LLM requests', ['model', 'status'])
REQUEST_DURATION = Histogram('llm_request_duration_seconds', 'Request duration', ['model'])
TOKENS_GENERATED = Counter('llm_tokens_generated_total', 'Total tokens generated', ['model'])
GPU_MEMORY_USAGE = Gauge('llm_gpu_memory_bytes', 'GPU memory usage', ['gpu_id'])
ACTIVE_REQUESTS = Gauge('llm_active_requests', 'Number of active requests')

# Request/Response models
class CompletionRequest(BaseModel):
    """LLM completion request."""
    prompt: str = Field(..., description="Input prompt")
    max_tokens: int = Field(512, ge=1, le=4096, description="Maximum tokens to generate")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: float = Field(0.95, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    top_k: int = Field(50, ge=1, le=100, description="Top-k sampling parameter")
    stop: Optional[List[str]] = Field(None, description="Stop sequences")
    stream: bool = Field(False, description="Enable streaming responses")

class CompletionResponse(BaseModel):
    """LLM completion response."""
    text: str
    tokens_generated: int
    latency_ms: float
    model: str

class LLMServer:
    """
    Production LLM server with vLLM backend.

    TODO: Implement LLM serving infrastructure
    """

    def __init__(
        self,
        model_name: str = "meta-llama/Llama-2-7b-chat-hf",
        tensor_parallel_size: int = 1,
        gpu_memory_utilization: float = 0.9,
        max_num_seqs: int = 256,
        quantization: Optional[str] = None,  # "awq", "gptq", or None
    ):
        """
        Initialize LLM server.

        Args:
            model_name: HuggingFace model identifier
            tensor_parallel_size: Number of GPUs for tensor parallelism
            gpu_memory_utilization: GPU memory utilization (0.0-1.0)
            max_num_seqs: Maximum number of sequences to batch
            quantization: Quantization method

        TODO: Initialize vLLM engine with optimizations
        """
        self.model_name = model_name
        self.tensor_parallel_size = tensor_parallel_size

        logging.info(f"Initializing LLM server with model: {model_name}")

        # TODO: Initialize AsyncLLMEngine
        # engine_args = AsyncEngineArgs(
        #     model=model_name,
        #     tensor_parallel_size=tensor_parallel_size,
        #     gpu_memory_utilization=gpu_memory_utilization,
        #     max_num_seqs=max_num_seqs,
        #     quantization=quantization,
        #     dtype="float16",  # or "bfloat16"
        #     trust_remote_code=True,
        # )

        # self.engine = AsyncLLMEngine.from_engine_args(engine_args)

        # TODO: Set up request tracking
        self.active_requests = {}
        self.request_lock = asyncio.Lock()

        logging.info("LLM server initialized successfully")

    async def generate(
        self,
        request: CompletionRequest,
        request_id: str
    ) -> CompletionResponse:
        """
        Generate completion for a request.

        TODO: Implement generation logic
        - Create sampling parameters
        - Submit request to engine
        - Track metrics
        - Handle errors
        """
        start_time = time.time()

        try:
            # TODO: Track active request
            ACTIVE_REQUESTS.inc()

            # TODO: Create sampling parameters
            # sampling_params = SamplingParams(
            #     temperature=request.temperature,
            #     top_p=request.top_p,
            #     top_k=request.top_k,
            #     max_tokens=request.max_tokens,
            #     stop=request.stop,
            # )

            # TODO: Generate completion
            # results_generator = self.engine.generate(
            #     request.prompt,
            #     sampling_params,
            #     request_id
            # )

            # TODO: Collect results
            # final_output = None
            # async for request_output in results_generator:
            #     final_output = request_output

            # TODO: Extract text and metrics
            # generated_text = final_output.outputs[0].text
            # tokens_generated = len(final_output.outputs[0].token_ids)

            # TODO: Calculate latency
            latency_ms = (time.time() - start_time) * 1000

            # TODO: Update metrics
            # REQUESTS_TOTAL.labels(model=self.model_name, status="success").inc()
            # REQUEST_DURATION.labels(model=self.model_name).observe(latency_ms / 1000)
            # TOKENS_GENERATED.labels(model=self.model_name).inc(tokens_generated)

            # return CompletionResponse(
            #     text=generated_text,
            #     tokens_generated=tokens_generated,
            #     latency_ms=latency_ms,
            #     model=self.model_name
            # )

            pass

        except Exception as e:
            logging.error(f"Generation failed for request {request_id}: {e}")
            REQUESTS_TOTAL.labels(model=self.model_name, status="error").inc()
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            ACTIVE_REQUESTS.dec()

    async def stream_generate(
        self,
        request: CompletionRequest,
        request_id: str
    ) -> AsyncIterator[str]:
        """
        Generate completion with streaming.

        TODO: Implement streaming generation
        - Stream tokens as they're generated
        - Handle client disconnections
        - Cleanup on errors
        """
        try:
            ACTIVE_REQUESTS.inc()

            # TODO: Create sampling parameters
            # sampling_params = SamplingParams(...)

            # TODO: Stream generation
            # results_generator = self.engine.generate(...)

            # async for request_output in results_generator:
            #     # Yield incremental text
            #     if request_output.outputs:
            #         text = request_output.outputs[0].text
            #         yield f"data: {text}\n\n"

            # yield "data: [DONE]\n\n"

            pass

        finally:
            ACTIVE_REQUESTS.dec()

    async def health_check(self) -> Dict[str, any]:
        """
        Check server health.

        TODO: Implement health check
        - Check GPU availability
        - Check model loaded
        - Return metrics
        """
        # TODO: Get GPU stats
        # import torch
        # gpu_stats = {
        #     f"gpu_{i}": {
        #         "memory_allocated": torch.cuda.memory_allocated(i),
        #         "memory_reserved": torch.cuda.memory_reserved(i),
        #         "utilization": torch.cuda.utilization(i)
        #     }
        #     for i in range(torch.cuda.device_count())
        # }

        # return {
        #     "status": "healthy",
        #     "model": self.model_name,
        #     "active_requests": ACTIVE_REQUESTS._value.get(),
        #     "total_requests": REQUESTS_TOTAL.labels(
        #         model=self.model_name, status="success"
        #     )._value.get(),
        #     "gpu_stats": gpu_stats
        # }

        pass


# FastAPI application
app = FastAPI(
    title="LLM Serving API",
    description="Production LLM serving with vLLM",
    version="1.0.0"
)

security = HTTPBearer()

# Global server instance
llm_server: Optional[LLMServer] = None

@app.on_event("startup")
async def startup_event():
    """Initialize LLM server on startup."""
    global llm_server

    # TODO: Initialize server with configuration
    # llm_server = LLMServer(
    #     model_name="meta-llama/Llama-2-7b-chat-hf",
    #     tensor_parallel_size=1,
    #     gpu_memory_utilization=0.9,
    #     quantization=None  # or "awq" for quantized models
    # )

    logging.info("LLM server started")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    global llm_server
    # TODO: Cleanup resources
    logging.info("LLM server shutdown")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verify authentication token.

    TODO: Implement token verification
    """
    # TODO: Verify token against database or JWT
    # if not is_valid_token(credentials.credentials):
    #     raise HTTPException(status_code=401, detail="Invalid token")

    # return credentials.credentials
    pass

@app.post("/v1/completions", response_model=CompletionResponse)
async def create_completion(
    request: CompletionRequest,
    token: str = Depends(verify_token)
):
    """
    Generate LLM completion.

    TODO: Handle completion request
    """
    if llm_server is None:
        raise HTTPException(status_code=503, detail="Server not initialized")

    # TODO: Generate unique request ID
    # request_id = f"req_{time.time_ns()}"

    # TODO: Generate completion
    # response = await llm_server.generate(request, request_id)
    # return response

    pass

@app.get("/v1/models")
async def list_models(token: str = Depends(verify_token)):
    """
    List available models.

    TODO: Return model information
    """
    # return {
    #     "models": [
    #         {
    #             "id": llm_server.model_name,
    #             "type": "text-generation",
    #             "tensor_parallel_size": llm_server.tensor_parallel_size
    #         }
    #     ]
    # }
    pass

@app.get("/health")
async def health():
    """Health check endpoint."""
    if llm_server is None:
        raise HTTPException(status_code=503, detail="Server not initialized")

    # return await llm_server.health_check()
    pass

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    from prometheus_client import generate_latest
    return generate_latest()


if __name__ == "__main__":
    # TODO: Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        workers=1  # vLLM uses its own parallelism
    )
```

```python
# llm_client.py
"""
Client for testing LLM serving API.
"""

import requests
import time
from typing import Optional

class LLMClient:
    """Client for LLM serving API."""

    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = ""):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def complete(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7,
        **kwargs
    ) -> dict:
        """
        Generate completion.

        TODO: Implement completion request
        """
        # TODO: Make request
        # response = requests.post(
        #     f"{self.base_url}/v1/completions",
        #     headers=self.headers,
        #     json={
        #         "prompt": prompt,
        #         "max_tokens": max_tokens,
        #         "temperature": temperature,
        #         **kwargs
        #     }
        # )

        # response.raise_for_status()
        # return response.json()

        pass

    def benchmark(self, prompt: str, num_requests: int = 10):
        """
        Benchmark server performance.

        TODO: Implement benchmarking
        - Send multiple requests
        - Measure latency
        - Calculate throughput
        """
        latencies = []

        for i in range(num_requests):
            start = time.time()
            # TODO: Send request
            # self.complete(prompt)
            latency = time.time() - start
            latencies.append(latency)

            print(f"Request {i+1}/{num_requests}: {latency:.2f}s")

        # TODO: Calculate statistics
        # avg_latency = sum(latencies) / len(latencies)
        # throughput = num_requests / sum(latencies)

        # print(f"\nResults:")
        # print(f"Average latency: {avg_latency:.2f}s")
        # print(f"Throughput: {throughput:.2f} requests/sec")

        pass


if __name__ == "__main__":
    # TODO: Test client
    # client = LLMClient(api_key="your-api-key")

    # Example usage
    # response = client.complete(
    #     prompt="What is machine learning?",
    #     max_tokens=256,
    #     temperature=0.7
    # )

    # print(response)

    # Benchmark
    # client.benchmark("Hello, world!", num_requests=10)
    pass
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install vLLM
RUN pip3 install vllm fastapi uvicorn prometheus-client

# TODO: Set up model cache directory
ENV HF_HOME=/models
VOLUME /models

# Copy application code
WORKDIR /app
COPY llm_serving.py .

# TODO: Expose port
EXPOSE 8000

# TODO: Set entrypoint
CMD ["python3", "llm_serving.py"]
```

### Success Criteria

- [ ] vLLM engine initializes successfully
- [ ] Model loads with quantization (if specified)
- [ ] API handles concurrent requests
- [ ] Metrics are tracked and exposed
- [ ] Health check endpoint works
- [ ] Latency is under 2 seconds for 512 tokens
- [ ] GPU memory is efficiently utilized
- [ ] Authentication works correctly

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **vLLM Installation**: Requires CUDA-compatible GPU, use `pip install vllm`
2. **Quantization**: Use AWQ or GPTQ for 4-bit quantization to reduce memory
3. **Batching**: Configure `max_num_seqs` based on GPU memory
4. **Tensor Parallelism**: Set to number of GPUs for multi-GPU serving
5. **Monitoring**: Use Prometheus metrics for production monitoring
6. **Caching**: vLLM automatically caches KV for efficiency

</details>

---

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

## Exercise 3: Edge ML Optimization (90 minutes)

**Objective**: Optimize ML models for edge deployment with quantization, pruning, and compilation techniques.

### Background

Edge ML requires:
- Model compression (quantization, pruning)
- Hardware-specific optimization
- Latency and memory constraints
- Battery efficiency considerations

### Tasks

1. **Implement quantization**:
   - Post-training quantization (PTQ)
   - Quantization-aware training (QAT)
   - Compare INT8 and FP16 performance
   - Measure accuracy degradation

2. **Apply model pruning**:
   - Structured pruning
   - Unstructured pruning
   - Gradual magnitude pruning
   - Fine-tuning after pruning

3. **Optimize for target hardware**:
   - Convert to TensorFlow Lite
   - Convert to ONNX Runtime
   - Optimize for specific hardware
   - Benchmark on target device

4. **Implement inference pipeline**:
   - Preprocessing optimization
   - Batch processing
   - Model caching
   - Power-aware scheduling

### Starter Code

```python
# edge_ml_optimization.py
"""
Edge ML model optimization with quantization and pruning.
"""

import tensorflow as tf
import tensorflow_model_optimization as tfmot
import numpy as np
from typing import Tuple, Optional, Dict
import logging
import time
from pathlib import Path

class ModelQuantizer:
    """
    Quantize models for edge deployment.

    TODO: Implement quantization techniques
    """

    def __init__(self, model: tf.keras.Model):
        """Initialize quantizer with model."""
        self.model = model
        self.quantized_model = None

    def post_training_quantization(
        self,
        representative_dataset: np.ndarray,
        quantization_type: str = "int8"  # "int8", "float16", "dynamic"
    ) -> tf.lite.TFLiteConverter:
        """
        Apply post-training quantization.

        TODO: Implement PTQ
        - Convert to TFLite
        - Apply quantization
        - Set optimization flags
        """
        # TODO: Create TFLite converter
        # converter = tf.lite.TFLiteConverter.from_keras_model(self.model)

        # TODO: Set optimization
        # if quantization_type == "int8":
        #     converter.optimizations = [tf.lite.Optimize.DEFAULT]
        #
        #     # Representative dataset for calibration
        #     def representative_dataset_gen():
        #         for sample in representative_dataset:
        #             yield [sample.astype(np.float32)]
        #
        #     converter.representative_dataset = representative_dataset_gen
        #     converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        #     converter.inference_input_type = tf.int8
        #     converter.inference_output_type = tf.int8

        # elif quantization_type == "float16":
        #     converter.optimizations = [tf.lite.Optimize.DEFAULT]
        #     converter.target_spec.supported_types = [tf.float16]

        # elif quantization_type == "dynamic":
        #     converter.optimizations = [tf.lite.Optimize.DEFAULT]

        # TODO: Convert model
        # self.quantized_model = converter.convert()

        # return converter

        pass

    def quantization_aware_training(
        self,
        train_data: Tuple[np.ndarray, np.ndarray],
        val_data: Tuple[np.ndarray, np.ndarray],
        epochs: int = 10
    ) -> tf.keras.Model:
        """
        Apply quantization-aware training.

        TODO: Implement QAT
        - Add quantization layers
        - Train with quantization simulation
        - Fine-tune model
        """
        # TODO: Create QAT model
        # quantize_model = tfmot.quantization.keras.quantize_model
        # qat_model = quantize_model(self.model)

        # TODO: Compile model
        # qat_model.compile(
        #     optimizer='adam',
        #     loss='sparse_categorical_crossentropy',
        #     metrics=['accuracy']
        # )

        # TODO: Train
        # history = qat_model.fit(
        #     train_data[0], train_data[1],
        #     batch_size=32,
        #     epochs=epochs,
        #     validation_data=val_data
        # )

        # TODO: Convert to TFLite
        # converter = tf.lite.TFLiteConverter.from_keras_model(qat_model)
        # converter.optimizations = [tf.lite.Optimize.DEFAULT]
        # self.quantized_model = converter.convert()

        # return qat_model

        pass

    def save_quantized_model(self, output_path: str):
        """
        Save quantized model.

        TODO: Save TFLite model
        """
        if self.quantized_model is None:
            raise ValueError("No quantized model available. Run quantization first.")

        # TODO: Save model
        # with open(output_path, 'wb') as f:
        #     f.write(self.quantized_model)

        # logging.info(f"Quantized model saved to {output_path}")

        pass

    def benchmark_quantized_model(
        self,
        test_data: np.ndarray,
        num_runs: int = 100
    ) -> Dict:
        """
        Benchmark quantized model performance.

        TODO: Measure latency and accuracy
        """
        if self.quantized_model is None:
            raise ValueError("No quantized model available")

        # TODO: Create interpreter
        # interpreter = tf.lite.Interpreter(model_content=self.quantized_model)
        # interpreter.allocate_tensors()

        # TODO: Get input/output details
        # input_details = interpreter.get_input_details()
        # output_details = interpreter.get_output_details()

        # TODO: Benchmark inference
        # latencies = []
        # for _ in range(num_runs):
        #     sample = test_data[np.random.randint(len(test_data))]
        #
        #     start = time.time()
        #     interpreter.set_tensor(input_details[0]['index'], sample[np.newaxis, ...])
        #     interpreter.invoke()
        #     output = interpreter.get_tensor(output_details[0]['index'])
        #     latency = time.time() - start
        #
        #     latencies.append(latency)

        # TODO: Calculate statistics
        # return {
        #     'avg_latency_ms': np.mean(latencies) * 1000,
        #     'p50_latency_ms': np.percentile(latencies, 50) * 1000,
        #     'p95_latency_ms': np.percentile(latencies, 95) * 1000,
        #     'p99_latency_ms': np.percentile(latencies, 99) * 1000,
        #     'throughput_qps': 1.0 / np.mean(latencies)
        # }

        pass


class ModelPruner:
    """
    Prune models for efficiency.

    TODO: Implement pruning techniques
    """

    def __init__(self, model: tf.keras.Model):
        """Initialize pruner with model."""
        self.model = model
        self.pruned_model = None

    def magnitude_pruning(
        self,
        train_data: Tuple[np.ndarray, np.ndarray],
        target_sparsity: float = 0.5,
        epochs: int = 10
    ) -> tf.keras.Model:
        """
        Apply magnitude-based pruning.

        TODO: Implement magnitude pruning
        - Define pruning schedule
        - Apply pruning to layers
        - Fine-tune pruned model
        """
        # TODO: Define pruning schedule
        # prune_low_magnitude = tfmot.sparsity.keras.prune_low_magnitude

        # pruning_params = {
        #     'pruning_schedule': tfmot.sparsity.keras.PolynomialDecay(
        #         initial_sparsity=0.0,
        #         final_sparsity=target_sparsity,
        #         begin_step=0,
        #         end_step=epochs * len(train_data[0]) // 32
        #     )
        # }

        # TODO: Apply pruning to model
        # self.pruned_model = prune_low_magnitude(self.model, **pruning_params)

        # TODO: Compile and train
        # self.pruned_model.compile(
        #     optimizer='adam',
        #     loss='sparse_categorical_crossentropy',
        #     metrics=['accuracy']
        # )

        # callbacks = [
        #     tfmot.sparsity.keras.UpdatePruningStep(),
        #     tfmot.sparsity.keras.PruningSummaries(log_dir='./logs')
        # ]

        # self.pruned_model.fit(
        #     train_data[0], train_data[1],
        #     batch_size=32,
        #     epochs=epochs,
        #     callbacks=callbacks
        # )

        # TODO: Strip pruning wrappers
        # self.pruned_model = tfmot.sparsity.keras.strip_pruning(self.pruned_model)

        # return self.pruned_model

        pass

    def structured_pruning(
        self,
        train_data: Tuple[np.ndarray, np.ndarray],
        pruning_ratio: float = 0.3
    ):
        """
        Apply structured pruning (remove entire channels/filters).

        TODO: Implement structured pruning
        """
        # TODO: Analyze layer importance
        # TODO: Remove least important channels
        # TODO: Fine-tune reduced model
        pass

    def measure_sparsity(self) -> float:
        """
        Measure model sparsity.

        TODO: Calculate percentage of zero weights
        """
        if self.pruned_model is None:
            model_to_check = self.model
        else:
            model_to_check = self.pruned_model

        # TODO: Count zero weights
        # total_weights = 0
        # zero_weights = 0

        # for layer in model_to_check.layers:
        #     if hasattr(layer, 'kernel'):
        #         weights = layer.kernel.numpy()
        #         total_weights += weights.size
        #         zero_weights += np.sum(weights == 0)

        # sparsity = zero_weights / total_weights
        # return sparsity

        pass


class EdgeMLPipeline:
    """
    Complete edge ML optimization pipeline.

    TODO: Implement end-to-end optimization
    """

    def __init__(self, model: tf.keras.Model):
        """Initialize pipeline."""
        self.original_model = model
        self.optimized_model = None
        self.quantizer = ModelQuantizer(model)
        self.pruner = ModelPruner(model)

    def optimize(
        self,
        train_data: Tuple[np.ndarray, np.ndarray],
        val_data: Tuple[np.ndarray, np.ndarray],
        test_data: np.ndarray,
        target_size_mb: float = 10.0,
        target_latency_ms: float = 100.0
    ) -> Dict:
        """
        Optimize model to meet constraints.

        TODO: Implement optimization pipeline
        - Apply pruning
        - Apply quantization
        - Measure metrics
        - Iterate if needed
        """
        logging.info("Starting edge ML optimization pipeline")

        # TODO: 1. Baseline metrics
        # baseline_metrics = self._evaluate_model(self.original_model, val_data)
        # logging.info(f"Baseline accuracy: {baseline_metrics['accuracy']:.4f}")

        # TODO: 2. Apply pruning
        # logging.info("Applying pruning...")
        # pruned_model = self.pruner.magnitude_pruning(
        #     train_data,
        #     target_sparsity=0.5,
        #     epochs=5
        # )

        # TODO: 3. Apply quantization
        # logging.info("Applying quantization...")
        # self.quantizer.model = pruned_model
        # self.quantizer.post_training_quantization(
        #     train_data[0][:100],
        #     quantization_type="int8"
        # )

        # TODO: 4. Benchmark optimized model
        # optimized_metrics = self.quantizer.benchmark_quantized_model(
        #     test_data,
        #     num_runs=100
        # )

        # TODO: 5. Calculate compression ratio
        # original_size = self._get_model_size(self.original_model)
        # optimized_size = len(self.quantizer.quantized_model) / (1024 * 1024)
        # compression_ratio = original_size / optimized_size

        # TODO: Return results
        # return {
        #     'baseline_accuracy': baseline_metrics['accuracy'],
        #     'optimized_latency_ms': optimized_metrics['avg_latency_ms'],
        #     'original_size_mb': original_size,
        #     'optimized_size_mb': optimized_size,
        #     'compression_ratio': compression_ratio,
        #     'meets_constraints': (
        #         optimized_size <= target_size_mb and
        #         optimized_metrics['avg_latency_ms'] <= target_latency_ms
        #     )
        # }

        pass

    def _evaluate_model(self, model: tf.keras.Model, data: Tuple) -> Dict:
        """Evaluate model accuracy."""
        # loss, accuracy = model.evaluate(data[0], data[1], verbose=0)
        # return {'loss': loss, 'accuracy': accuracy}
        pass

    def _get_model_size(self, model: tf.keras.Model) -> float:
        """Get model size in MB."""
        # temp_path = '/tmp/temp_model.h5'
        # model.save(temp_path)
        # size_mb = Path(temp_path).stat().st_size / (1024 * 1024)
        # Path(temp_path).unlink()
        # return size_mb
        pass


# Example usage
if __name__ == "__main__":
    # TODO: Create sample model
    # model = tf.keras.Sequential([
    #     tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
    #     tf.keras.layers.MaxPooling2D(),
    #     tf.keras.layers.Conv2D(64, 3, activation='relu'),
    #     tf.keras.layers.MaxPooling2D(),
    #     tf.keras.layers.Flatten(),
    #     tf.keras.layers.Dense(128, activation='relu'),
    #     tf.keras.layers.Dense(10, activation='softmax')
    # ])

    # TODO: Load data (e.g., MNIST)
    # (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    # x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255
    # x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255

    # TODO: Train baseline model
    # model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    # model.fit(x_train, y_train, epochs=5, validation_split=0.2)

    # TODO: Optimize for edge
    # pipeline = EdgeMLPipeline(model)
    # results = pipeline.optimize(
    #     train_data=(x_train, y_train),
    #     val_data=(x_test, y_test),
    #     test_data=x_test,
    #     target_size_mb=5.0,
    #     target_latency_ms=50.0
    # )

    # print(results)

    pass
```

### Success Criteria

- [ ] Model size reduced by >4x through quantization
- [ ] Pruning achieves >50% sparsity
- [ ] Accuracy degradation < 2% from baseline
- [ ] Inference latency meets target
- [ ] TFLite model runs on mobile/edge device
- [ ] Power consumption measured and optimized

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Quantization**: Start with dynamic quantization, then PTQ, then QAT if needed
2. **Pruning**: Apply gradual magnitude pruning during fine-tuning
3. **Evaluation**: Test on actual target hardware, simulators can be misleading
4. **Accuracy**: Monitor accuracy at each optimization step
5. **Combined**: Prune first, then quantize for best results
6. **Hardware**: Use TFLite delegates for GPU/NPU acceleration

</details>

---

## Exercise 4: AutoML Pipeline (90 minutes)

**Objective**: Build an automated machine learning pipeline with hyperparameter optimization, architecture search, and model selection.

### Background

AutoML automates:
- Hyperparameter tuning
- Feature engineering
- Model selection
- Architecture search
- Ensemble creation

### Tasks

1. **Implement hyperparameter optimization**:
   - Use Optuna for optimization
   - Define search space
   - Implement pruning
   - Track experiments

2. **Build AutoML pipeline**:
   - Automated preprocessing
   - Model selection
   - Feature selection
   - Ensemble methods

3. **Create neural architecture search**:
   - Define search space
   - Implement search strategy
   - Evaluate candidates
   - Select best architecture

4. **Add experiment tracking**:
   - Log all trials
   - Visualize results
   - Compare models
   - Export best model

### Starter Code

```python
# automl_pipeline.py
"""
AutoML pipeline with Optuna for hyperparameter optimization.
"""

import optuna
from optuna.pruners import MedianPruner
from optuna.samplers import TPESampler
import mlflow
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime

class AutoMLPipeline:
    """
    Automated ML pipeline with hyperparameter optimization.

    TODO: Implement complete AutoML system
    """

    def __init__(
        self,
        task: str = "classification",  # "classification" or "regression"
        metric: str = "accuracy",
        n_trials: int = 100,
        timeout: int = 3600,  # seconds
        mlflow_tracking_uri: str = "http://localhost:5000"
    ):
        """
        Initialize AutoML pipeline.

        Args:
            task: ML task type
            metric: Optimization metric
            n_trials: Number of optimization trials
            timeout: Optimization timeout in seconds
            mlflow_tracking_uri: MLflow tracking server URI

        TODO: Set up AutoML configuration
        """
        self.task = task
        self.metric = metric
        self.n_trials = n_trials
        self.timeout = timeout

        # TODO: Set up MLflow
        # mlflow.set_tracking_uri(mlflow_tracking_uri)
        # mlflow.set_experiment("automl_optimization")

        # TODO: Initialize study
        # self.study = None
        # self.best_model = None
        # self.best_params = None

        logging.info(f"AutoML pipeline initialized for {task} task")

    def create_objective(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray
    ):
        """
        Create Optuna objective function.

        TODO: Implement objective function
        - Suggest hyperparameters
        - Train model
        - Evaluate performance
        - Return metric
        """
        def objective(trial: optuna.Trial) -> float:
            """
            Objective function for optimization.

            TODO: Implement objective
            """
            # TODO: Start MLflow run
            with mlflow.start_run(nested=True):
                # TODO: Suggest model type
                # model_name = trial.suggest_categorical(
                #     'model',
                #     ['random_forest', 'gradient_boosting', 'svm']
                # )

                # TODO: Suggest hyperparameters based on model
                # if model_name == 'random_forest':
                #     params = {
                #         'n_estimators': trial.suggest_int('n_estimators', 50, 500),
                #         'max_depth': trial.suggest_int('max_depth', 3, 20),
                #         'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
                #         'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
                #         'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2']),
                #         'random_state': 42
                #     }
                #     model = RandomForestClassifier(**params)

                # elif model_name == 'gradient_boosting':
                #     params = {
                #         'n_estimators': trial.suggest_int('n_estimators', 50, 300),
                #         'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
                #         'max_depth': trial.suggest_int('max_depth', 3, 10),
                #         'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
                #         'subsample': trial.suggest_float('subsample', 0.6, 1.0),
                #         'random_state': 42
                #     }
                #     model = GradientBoostingClassifier(**params)

                # elif model_name == 'svm':
                #     params = {
                #         'C': trial.suggest_float('C', 0.1, 100, log=True),
                #         'kernel': trial.suggest_categorical('kernel', ['rbf', 'poly']),
                #         'gamma': trial.suggest_categorical('gamma', ['scale', 'auto']),
                #         'random_state': 42
                #     }
                #     model = SVC(**params)

                # TODO: Suggest preprocessing
                # use_scaling = trial.suggest_categorical('use_scaling', [True, False])
                # if use_scaling:
                #     scaler = StandardScaler()
                #     X_train_processed = scaler.fit_transform(X_train)
                #     X_val_processed = scaler.transform(X_val)
                # else:
                #     X_train_processed = X_train
                #     X_val_processed = X_val

                # TODO: Feature selection
                # n_features = trial.suggest_int('n_features', 10, X_train.shape[1])
                # selector = SelectKBest(f_classif, k=n_features)
                # X_train_processed = selector.fit_transform(X_train_processed, y_train)
                # X_val_processed = selector.transform(X_val_processed)

                # TODO: Train model
                # model.fit(X_train_processed, y_train)

                # TODO: Evaluate
                # y_pred = model.predict(X_val_processed)
                # score = accuracy_score(y_val, y_pred)

                # TODO: Log parameters and metrics to MLflow
                # mlflow.log_params(params)
                # mlflow.log_param('model_type', model_name)
                # mlflow.log_metric('accuracy', score)

                # TODO: Pruning - report intermediate value
                # trial.report(score, step=1)

                # if trial.should_prune():
                #     raise optuna.TrialPruned()

                # return score

                pass

        return objective

    def optimize(
        self,
        X: np.ndarray,
        y: np.ndarray,
        test_size: float = 0.2
    ) -> Dict:
        """
        Run AutoML optimization.

        TODO: Implement optimization loop
        - Split data
        - Create study
        - Run optimization
        - Return best model and params
        """
        # TODO: Split data
        # X_train, X_val, y_train, y_val = train_test_split(
        #     X, y, test_size=test_size, random_state=42, stratify=y
        # )

        # TODO: Create objective
        # objective = self.create_objective(X_train, y_train, X_val, y_val)

        # TODO: Create study with pruning
        # sampler = TPESampler(seed=42)
        # pruner = MedianPruner(n_startup_trials=5, n_warmup_steps=10)

        # self.study = optuna.create_study(
        #     direction='maximize',
        #     sampler=sampler,
        #     pruner=pruner,
        #     study_name=f"automl_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        # )

        # TODO: Run optimization
        # logging.info(f"Starting optimization with {self.n_trials} trials")

        # with mlflow.start_run(run_name="automl_optimization"):
        #     self.study.optimize(
        #         objective,
        #         n_trials=self.n_trials,
        #         timeout=self.timeout,
        #         show_progress_bar=True
        #     )

        #     # TODO: Get best trial
        #     best_trial = self.study.best_trial
        #     self.best_params = best_trial.params

        #     # TODO: Log best params to MLflow
        #     mlflow.log_params(self.best_params)
        #     mlflow.log_metric('best_score', best_trial.value)

        #     # TODO: Train final model with best params
        #     self.best_model = self._train_best_model(X_train, y_train)

        #     # TODO: Evaluate on validation set
        #     val_score = self._evaluate_model(self.best_model, X_val, y_val)
        #     mlflow.log_metric('val_score', val_score)

        #     # TODO: Log model
        #     mlflow.sklearn.log_model(self.best_model, "best_model")

        # TODO: Return results
        # return {
        #     'best_params': self.best_params,
        #     'best_score': best_trial.value,
        #     'n_trials': len(self.study.trials),
        #     'study': self.study
        # }

        pass

    def _train_best_model(self, X: np.ndarray, y: np.ndarray):
        """
        Train model with best parameters.

        TODO: Recreate best model and train
        """
        # TODO: Extract model type and params
        # model_name = self.best_params['model']

        # TODO: Create model with best params
        # TODO: Apply preprocessing if specified
        # TODO: Train model

        pass

    def _evaluate_model(self, model, X: np.ndarray, y: np.ndarray) -> float:
        """Evaluate model on data."""
        # predictions = model.predict(X)
        # if self.metric == 'accuracy':
        #     from sklearn.metrics import accuracy_score
        #     return accuracy_score(y, predictions)
        # TODO: Add other metrics
        pass

    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance from best model.

        TODO: Extract and return feature importances
        """
        if self.best_model is None:
            raise ValueError("No model trained yet")

        # TODO: Get feature importance
        # if hasattr(self.best_model, 'feature_importances_'):
        #     importances = self.best_model.feature_importances_
        #
        #     return pd.DataFrame({
        #         'feature': range(len(importances)),
        #         'importance': importances
        #     }).sort_values('importance', ascending=False)

        pass

    def plot_optimization_history(self):
        """
        Visualize optimization history.

        TODO: Create visualization of trials
        """
        if self.study is None:
            raise ValueError("No study available")

        # TODO: Plot optimization history
        # import matplotlib.pyplot as plt
        # from optuna.visualization import plot_optimization_history, plot_param_importances

        # fig1 = plot_optimization_history(self.study)
        # fig1.show()

        # fig2 = plot_param_importances(self.study)
        # fig2.show()

        pass


# Neural Architecture Search
class NeuralArchitectureSearch:
    """
    Neural Architecture Search with Optuna.

    TODO: Implement NAS
    """

    def __init__(self, input_shape: Tuple, num_classes: int):
        """Initialize NAS."""
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.best_model = None

    def create_model(self, trial: optuna.Trial):
        """
        Create model based on trial suggestions.

        TODO: Implement architecture search space
        - Number of layers
        - Layer types
        - Activation functions
        - Regularization
        """
        import tensorflow as tf

        # TODO: Create sequential model
        # model = tf.keras.Sequential()
        # model.add(tf.keras.layers.Input(shape=self.input_shape))

        # TODO: Suggest number of layers
        # n_layers = trial.suggest_int('n_layers', 1, 5)

        # for i in range(n_layers):
        #     # TODO: Suggest layer type
        #     layer_type = trial.suggest_categorical(f'layer_{i}_type', ['dense', 'conv'])
        #
        #     if layer_type == 'dense':
        #         # TODO: Suggest units
        #         n_units = trial.suggest_int(f'layer_{i}_units', 32, 512, log=True)
        #         model.add(tf.keras.layers.Dense(n_units))
        #
        #     # TODO: Suggest activation
        #     activation = trial.suggest_categorical(f'layer_{i}_activation', ['relu', 'tanh'])
        #     model.add(tf.keras.layers.Activation(activation))
        #
        #     # TODO: Suggest dropout
        #     dropout = trial.suggest_float(f'layer_{i}_dropout', 0.0, 0.5)
        #     if dropout > 0:
        #         model.add(tf.keras.layers.Dropout(dropout))

        # TODO: Output layer
        # model.add(tf.keras.layers.Dense(self.num_classes, activation='softmax'))

        # TODO: Suggest optimizer and learning rate
        # learning_rate = trial.suggest_float('learning_rate', 1e-5, 1e-1, log=True)
        # optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

        # model.compile(
        #     optimizer=optimizer,
        #     loss='sparse_categorical_crossentropy',
        #     metrics=['accuracy']
        # )

        # return model

        pass

    def search(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        n_trials: int = 50
    ):
        """
        Run architecture search.

        TODO: Implement NAS optimization
        """
        def objective(trial):
            # TODO: Create model
            # model = self.create_model(trial)

            # TODO: Train model
            # history = model.fit(
            #     X_train, y_train,
            #     validation_data=(X_val, y_val),
            #     epochs=10,
            #     batch_size=32,
            #     verbose=0
            # )

            # TODO: Return validation accuracy
            # return history.history['val_accuracy'][-1]

            pass

        # TODO: Create and run study
        # study = optuna.create_study(direction='maximize')
        # study.optimize(objective, n_trials=n_trials)

        # TODO: Train best model
        # self.best_model = self.create_model(study.best_trial)

        pass


# Example usage
if __name__ == "__main__":
    # TODO: Load data
    # from sklearn.datasets import load_digits
    # X, y = load_digits(return_X_y=True)

    # TODO: Run AutoML
    # automl = AutoMLPipeline(
    #     task="classification",
    #     metric="accuracy",
    #     n_trials=50,
    #     timeout=1800
    # )

    # results = automl.optimize(X, y)
    # print(f"Best score: {results['best_score']:.4f}")
    # print(f"Best params: {results['best_params']}")

    # TODO: Visualize
    # automl.plot_optimization_history()

    pass
```

### Success Criteria

- [ ] Optuna optimization runs successfully
- [ ] Multiple models and hyperparameters explored
- [ ] Pruning reduces unnecessary trials
- [ ] Best model identified and logged to MLflow
- [ ] Performance improved over baseline
- [ ] Visualization of optimization process
- [ ] NAS finds optimal architecture

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Search Space**: Define broad initial space, narrow based on results
2. **Pruning**: Use MedianPruner to stop unpromising trials early
3. **Parallel**: Run with `n_jobs=-1` for parallel optimization
4. **Sampling**: TPESampler generally works best
5. **MLflow**: Log every trial for complete experiment tracking
6. **Ensembles**: Combine top-k models for better performance

</details>

---

## Exercise 5: Real-time ML with Feature Stores (120 minutes)

**Objective**: Build a real-time ML system with Feast feature store for online serving and feature management.

### Background

Real-time ML requires:
- Low-latency feature serving
- Consistent features (training/serving)
- Feature versioning and monitoring
- Online and offline feature stores
- Point-in-time correct features

### Tasks

1. **Set up Feast feature store**:
   - Install and configure Feast
   - Define feature views
   - Set up online/offline stores
   - Implement materialization

2. **Create feature pipelines**:
   - Define data sources
   - Create feature transformations
   - Implement feature validation
   - Set up feature monitoring

3. **Build online serving**:
   - Deploy online feature store
   - Implement feature retrieval API
   - Add caching layer
   - Optimize for latency

4. **Integrate with ML pipeline**:
   - Training with offline features
   - Serving with online features
   - Feature drift detection
   - Automated retraining triggers

### Starter Code

```python
# feast_feature_store.py
"""
Real-time ML with Feast feature store.
"""

from feast import FeatureStore, Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64, String
from feast.on_demand_feature_view import on_demand_feature_view
from feast.value_type import ValueType
from datetime import timedelta, datetime
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
import redis

# Feature definitions
class FeatureDefinitions:
    """
    Define features for the feature store.

    TODO: Implement feature definitions
    """

    @staticmethod
    def create_user_entity() -> Entity:
        """
        Create user entity.

        TODO: Define user entity
        """
        # return Entity(
        #     name="user",
        #     join_keys=["user_id"],
        #     description="User entity"
        # )
        pass

    @staticmethod
    def create_user_features(data_source: FileSource) -> FeatureView:
        """
        Create user feature view.

        TODO: Define user features
        - Age
        - Account age
        - Transaction count
        - Average transaction amount
        """
        # return FeatureView(
        #     name="user_features",
        #     entities=["user"],
        #     ttl=timedelta(days=1),
        #     schema=[
        #         Field(name="age", dtype=Int64),
        #         Field(name="account_age_days", dtype=Int64),
        #         Field(name="transaction_count_30d", dtype=Int64),
        #         Field(name="avg_transaction_amount_30d", dtype=Float32),
        #         Field(name="is_premium", dtype=Int64),
        #     ],
        #     source=data_source,
        # )
        pass

    @staticmethod
    def create_transaction_features(data_source: FileSource) -> FeatureView:
        """
        Create transaction feature view.

        TODO: Define transaction features
        """
        # return FeatureView(
        #     name="transaction_features",
        #     entities=["user"],
        #     ttl=timedelta(hours=1),
        #     schema=[
        #         Field(name="transaction_amount", dtype=Float32),
        #         Field(name="merchant_category", dtype=String),
        #         Field(name="transaction_hour", dtype=Int64),
        #         Field(name="is_international", dtype=Int64),
        #     ],
        #     source=data_source,
        # )
        pass

    @staticmethod
    @on_demand_feature_view(
        sources=[],  # TODO: Add source feature views
        schema=[
            Field(name="transaction_to_avg_ratio", dtype=Float32),
            Field(name="is_high_value", dtype=Int64),
        ]
    )
    def derived_features(features_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create on-demand derived features.

        TODO: Implement feature transformations
        - Transaction to average ratio
        - High value transaction flag
        - Risk score
        """
        # df = pd.DataFrame()

        # TODO: Calculate derived features
        # df["transaction_to_avg_ratio"] = (
        #     features_df["transaction_amount"] /
        #     features_df["avg_transaction_amount_30d"]
        # )

        # df["is_high_value"] = (
        #     features_df["transaction_amount"] > 1000
        # ).astype(int)

        # return df

        pass


class FeastFeatureStore:
    """
    Wrapper for Feast feature store operations.

    TODO: Implement feature store management
    """

    def __init__(self, repo_path: str = "./feature_repo"):
        """
        Initialize feature store.

        Args:
            repo_path: Path to Feast repository

        TODO: Initialize Feast store
        """
        self.repo_path = repo_path
        # self.store = FeatureStore(repo_path=repo_path)

        logging.info(f"Feature store initialized at {repo_path}")

    def setup_feature_store(self):
        """
        Set up feature store with initial configuration.

        TODO: Implement setup
        - Create entities
        - Define feature views
        - Configure online/offline stores
        - Apply configuration
        """
        # TODO: Create data sources
        # user_source = FileSource(
        #     path="data/user_features.parquet",
        #     timestamp_field="event_timestamp",
        # )

        # transaction_source = FileSource(
        #     path="data/transaction_features.parquet",
        #     timestamp_field="event_timestamp",
        # )

        # TODO: Create entities and feature views
        # user_entity = FeatureDefinitions.create_user_entity()
        # user_fv = FeatureDefinitions.create_user_features(user_source)
        # transaction_fv = FeatureDefinitions.create_transaction_features(transaction_source)

        # TODO: Apply to store
        # self.store.apply([user_entity, user_fv, transaction_fv])

        logging.info("Feature store setup complete")

    def materialize_features(
        self,
        start_date: datetime,
        end_date: datetime
    ):
        """
        Materialize features to online store.

        TODO: Implement materialization
        - Load features from offline store
        - Push to online store (Redis)
        - Verify materialization
        """
        # TODO: Materialize features
        # self.store.materialize(
        #     start_date=start_date,
        #     end_date=end_date
        # )

        # logging.info(f"Materialized features from {start_date} to {end_date}")

        pass

    def get_online_features(
        self,
        entity_rows: List[Dict],
        features: List[str]
    ) -> pd.DataFrame:
        """
        Get features for online serving.

        TODO: Implement online feature retrieval
        - Fetch from online store
        - Handle missing features
        - Return as DataFrame
        """
        # TODO: Get features
        # feature_vector = self.store.get_online_features(
        #     features=features,
        #     entity_rows=entity_rows
        # )

        # TODO: Convert to DataFrame
        # return feature_vector.to_df()

        pass

    def get_historical_features(
        self,
        entity_df: pd.DataFrame,
        features: List[str]
    ) -> pd.DataFrame:
        """
        Get historical features for training.

        TODO: Implement offline feature retrieval
        - Perform point-in-time join
        - Return training dataset
        """
        # TODO: Get historical features
        # training_df = self.store.get_historical_features(
        #     entity_df=entity_df,
        #     features=features
        # ).to_df()

        # return training_df

        pass

    def validate_features(
        self,
        feature_df: pd.DataFrame,
        feature_names: List[str]
    ) -> Dict:
        """
        Validate feature quality.

        TODO: Implement feature validation
        - Check for nulls
        - Validate distributions
        - Detect outliers
        - Check freshness
        """
        validation_results = {}

        for feature in feature_names:
            if feature not in feature_df.columns:
                validation_results[feature] = {"status": "missing"}
                continue

            # TODO: Calculate validation metrics
            # null_pct = feature_df[feature].isnull().mean()
            # validation_results[feature] = {
            #     "status": "valid" if null_pct < 0.1 else "invalid",
            #     "null_percentage": null_pct,
            #     "mean": feature_df[feature].mean() if pd.api.types.is_numeric_dtype(feature_df[feature]) else None,
            #     "std": feature_df[feature].std() if pd.api.types.is_numeric_dtype(feature_df[feature]) else None
            # }

        return validation_results


class RealtimeMLPipeline:
    """
    Real-time ML pipeline with feature store.

    TODO: Implement end-to-end real-time ML
    """

    def __init__(
        self,
        feature_store: FeastFeatureStore,
        model_path: Optional[str] = None
    ):
        """Initialize pipeline."""
        self.feature_store = feature_store
        self.model = None

        # TODO: Load model if provided
        # if model_path:
        #     import joblib
        #     self.model = joblib.load(model_path)

    def train(
        self,
        entity_df: pd.DataFrame,
        features: List[str],
        target_column: str
    ):
        """
        Train model using historical features.

        TODO: Implement training with feature store
        - Get historical features
        - Prepare training data
        - Train model
        - Log to MLflow
        """
        logging.info("Starting training with historical features")

        # TODO: Get historical features
        # training_df = self.feature_store.get_historical_features(
        #     entity_df=entity_df,
        #     features=features
        # )

        # TODO: Prepare X, y
        # feature_columns = [f.split(':')[1] for f in features]
        # X = training_df[feature_columns]
        # y = training_df[target_column]

        # TODO: Train model
        # from sklearn.ensemble import RandomForestClassifier
        # self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        # self.model.fit(X, y)

        # TODO: Validate features
        # validation_results = self.feature_store.validate_features(
        #     training_df,
        #     feature_columns
        # )
        # logging.info(f"Feature validation: {validation_results}")

        logging.info("Training complete")

    def predict(
        self,
        user_ids: List[int],
        features: List[str]
    ) -> np.ndarray:
        """
        Make real-time predictions.

        TODO: Implement online prediction
        - Get online features
        - Make predictions
        - Log prediction latency
        """
        if self.model is None:
            raise ValueError("Model not trained or loaded")

        import time
        start = time.time()

        # TODO: Prepare entity rows
        # entity_rows = [{"user_id": user_id} for user_id in user_ids]

        # TODO: Get online features
        # feature_df = self.feature_store.get_online_features(
        #     entity_rows=entity_rows,
        #     features=features
        # )

        # TODO: Make predictions
        # feature_columns = [f.split(':')[1] for f in features]
        # X = feature_df[feature_columns]
        # predictions = self.model.predict(X)

        latency = time.time() - start
        logging.info(f"Prediction latency: {latency*1000:.2f}ms for {len(user_ids)} users")

        # return predictions

        pass

    def monitor_feature_drift(
        self,
        current_features: pd.DataFrame,
        reference_features: pd.DataFrame,
        feature_names: List[str]
    ) -> Dict:
        """
        Monitor feature drift.

        TODO: Implement drift detection
        - Calculate distribution differences
        - Detect statistical drift
        - Alert on significant drift
        """
        from scipy import stats

        drift_results = {}

        for feature in feature_names:
            # TODO: Calculate KS statistic
            # ks_stat, p_value = stats.ks_2samp(
            #     reference_features[feature],
            #     current_features[feature]
            # )

            # drift_results[feature] = {
            #     'ks_statistic': ks_stat,
            #     'p_value': p_value,
            #     'drift_detected': p_value < 0.05
            # }

            pass

        return drift_results


# FastAPI serving endpoint
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Real-time ML API")

# Global instances
feature_store: Optional[FeastFeatureStore] = None
ml_pipeline: Optional[RealtimeMLPipeline] = None

class PredictionRequest(BaseModel):
    user_ids: List[int]

class PredictionResponse(BaseModel):
    predictions: List[float]
    latency_ms: float

@app.on_event("startup")
async def startup():
    """Initialize feature store and model on startup."""
    global feature_store, ml_pipeline

    # TODO: Initialize feature store
    # feature_store = FeastFeatureStore(repo_path="./feature_repo")
    # ml_pipeline = RealtimeMLPipeline(
    #     feature_store=feature_store,
    #     model_path="./model.pkl"
    # )

    logging.info("Real-time ML API started")

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Make real-time predictions.

    TODO: Implement prediction endpoint
    """
    import time
    start = time.time()

    try:
        # TODO: Get features and predict
        # features = [
        #     "user_features:age",
        #     "user_features:transaction_count_30d",
        #     "user_features:avg_transaction_amount_30d"
        # ]

        # predictions = ml_pipeline.predict(
        #     user_ids=request.user_ids,
        #     features=features
        # )

        latency = (time.time() - start) * 1000

        # return PredictionResponse(
        #     predictions=predictions.tolist(),
        #     latency_ms=latency
        # )

        pass

    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}


if __name__ == "__main__":
    # TODO: Example usage

    # 1. Setup feature store
    # fs = FeastFeatureStore(repo_path="./feature_repo")
    # fs.setup_feature_store()

    # 2. Materialize features
    # fs.materialize_features(
    #     start_date=datetime(2024, 1, 1),
    #     end_date=datetime(2024, 1, 31)
    # )

    # 3. Train model
    # entity_df = pd.DataFrame({
    #     'user_id': [1, 2, 3, 4, 5],
    #     'event_timestamp': [datetime.now()] * 5,
    #     'fraud_label': [0, 0, 1, 0, 1]
    # })

    # pipeline = RealtimeMLPipeline(feature_store=fs)
    # pipeline.train(
    #     entity_df=entity_df,
    #     features=["user_features:age", "user_features:transaction_count_30d"],
    #     target_column="fraud_label"
    # )

    # 4. Make predictions
    # predictions = pipeline.predict(
    #     user_ids=[1, 2, 3],
    #     features=["user_features:age", "user_features:transaction_count_30d"]
    # )

    pass
```

```yaml
# feature_store.yaml
# Feast feature store configuration

project: realtime_ml
registry: data/registry.db
provider: local
online_store:
  type: redis
  connection_string: "localhost:6379"
offline_store:
  type: file
```

### Success Criteria

- [ ] Feast feature store is configured correctly
- [ ] Features are materialized to online store
- [ ] Online feature retrieval is under 50ms
- [ ] Historical features support point-in-time joins
- [ ] Training and serving use same features
- [ ] Feature drift is detected
- [ ] Real-time predictions work end-to-end

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Online Store**: Use Redis for low-latency feature serving
2. **Offline Store**: Use Parquet files or data warehouse
3. **Materialization**: Schedule regular materialization jobs
4. **Features**: Define features with proper TTL
5. **Monitoring**: Track feature freshness and drift
6. **Caching**: Add caching layer for frequently accessed features

</details>

---

## Submission Guidelines

For each exercise, submit:
1. **Code**: All implementation files with TODOs completed
2. **Documentation**: Architecture decisions and design choices
3. **Benchmarks**: Performance metrics and comparisons
4. **Screenshots**: Successful runs and visualizations
5. **Reflection**: Challenges faced and lessons learned

**Estimated Total Time**: 7.5 hours
**Difficulty**: Advanced

Good luck!
