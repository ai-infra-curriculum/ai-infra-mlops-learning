FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
RUN groupadd -r app && useradd -r -g app app
WORKDIR /app
COPY --from=builder /root/.local /home/app/.local
COPY --chown=app:app src/ ./src/
COPY --chown=app:app prompts/ ./prompts/
USER app
ENV PATH=/home/app/.local/bin:$PATH PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
