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
