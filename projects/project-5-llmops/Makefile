.PHONY: install test lint up down logs vllm

install:
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f api

# Spin up a vLLM server on the host for local testing (requires GPU + NVIDIA toolkit)
vllm:
	docker run --gpus all -p 8002:8000 \
	  vllm/vllm-openai:latest \
	  --model mistralai/Mistral-7B-Instruct-v0.2 \
	  --enable-prefix-caching
