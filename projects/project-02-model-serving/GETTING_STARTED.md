# Getting Started: Production Model Serving Platform

## Prerequisites

### Required Software
- Python 3.11 or higher
- Docker 24.0+
- Kubernetes 1.24+ (Minikube or Kind for local)
- kubectl
- Helm 3.0+
- Git

### Optional Tools
- k9s (Kubernetes CLI)
- Lens (Kubernetes IDE)
- Postman/Insomnia (API testing)
- Grafana K6 (load testing alternative)

### System Requirements
- **CPU**: 4+ cores
- **RAM**: 16GB+ (for local Kubernetes)
- **Disk**: 50GB+ free space

## Local Development Setup

### Step 1: Clone and Setup Environment

```bash
# Navigate to project directory
cd /path/to/project-02-model-serving

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configurations
```

### Step 2: Start Local Dependencies

```bash
# Start local services with Docker Compose
docker-compose up -d

# This starts:
# - PostgreSQL (metadata database)
# - Redis (cache)
# - MinIO (S3-compatible storage)
# - Vault (secrets management)
# - Prometheus (metrics)
# - Grafana (dashboards)
```

### Step 3: Initialize Vault

```bash
# Initialize and unseal Vault
./scripts/init-vault.sh

# This will:
# - Initialize Vault
# - Unseal Vault
# - Create policies
# - Store secrets
# - Output root token (save this!)
```

### Step 4: Setup Database

```bash
# Run database migrations
python scripts/init-db.py

# Load sample models metadata
python scripts/load-sample-models.py
```

### Step 5: Download Sample Models

```bash
# Download pre-trained ONNX models
python scripts/download-models.py

# This downloads:
# - ResNet-50 (image classification)
# - BERT (text classification)
# - XGBoost (tabular prediction)
```

### Step 6: Run the Application

```bash
# Start the FastAPI server
uvicorn src.api.server:app --reload --host 0.0.0.0 --port 8000

# Or use the script
./scripts/run-local.sh
```

### Step 7: Verify Setup

```bash
# Check health
curl http://localhost:8000/health

# List models
curl http://localhost:8000/models

# Test prediction
curl -X POST http://localhost:8000/predict/sample-model \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0]}'
```

## Kubernetes Deployment

### Step 1: Start Local Kubernetes

```bash
# Using Minikube
minikube start --cpus=4 --memory=8192 --driver=docker

# Or using Kind
kind create cluster --config infrastructure/kubernetes/kind-config.yaml

# Verify cluster
kubectl cluster-info
kubectl get nodes
```

### Step 2: Create Namespace

```bash
# Create namespace
kubectl create namespace model-serving

# Set as default
kubectl config set-context --current --namespace=model-serving
```

### Step 3: Deploy Dependencies

```bash
# Add Helm repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack \
  -f infrastructure/prometheus/values.yaml \
  --namespace model-serving

# Install Vault
helm install vault hashicorp/vault \
  -f infrastructure/vault/values.yaml \
  --namespace model-serving

# Install PostgreSQL
helm install postgresql bitnami/postgresql \
  -f infrastructure/kubernetes/postgresql-values.yaml \
  --namespace model-serving

# Install Redis
helm install redis bitnami/redis \
  -f infrastructure/kubernetes/redis-values.yaml \
  --namespace model-serving
```

### Step 4: Configure Secrets

```bash
# Create secrets from Vault
kubectl create secret generic model-server-secrets \
  --from-literal=database-url=postgresql://user:pass@postgresql:5432/models \
  --from-literal=redis-url=redis://redis:6379 \
  --namespace model-serving

# Or use Vault operator
kubectl apply -f infrastructure/kubernetes/vault-secret.yaml
```

### Step 5: Deploy Application

```bash
# Apply ConfigMaps
kubectl apply -f infrastructure/kubernetes/configmap.yaml

# Deploy application
kubectl apply -f infrastructure/kubernetes/deployment.yaml

# Create service
kubectl apply -f infrastructure/kubernetes/service.yaml

# Setup ingress
kubectl apply -f infrastructure/kubernetes/ingress.yaml

# Configure HPA
kubectl apply -f infrastructure/kubernetes/hpa.yaml
```

### Step 6: Verify Deployment

```bash
# Check pods
kubectl get pods

# Check services
kubectl get svc

# Check HPA
kubectl get hpa

# View logs
kubectl logs -f deployment/model-server

# Port forward for testing
kubectl port-forward svc/model-server 8000:80
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test suite
pytest tests/unit/
pytest tests/integration/
pytest tests/load/

# Run with markers
pytest -m "not slow"
pytest -m "integration"
```

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/
pylint src/

# Type checking
mypy src/

# Security scan
bandit -r src/

# Run all checks
./scripts/check-code.sh
```

### Making Changes

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes and test
# ... edit files ...
pytest

# Format and lint
black src/
flake8 src/

# Commit changes
git add .
git commit -m "feat: your feature description"

# Push and create PR
git push origin feature/your-feature
```

### Local Testing with Hot Reload

```bash
# Start with auto-reload
uvicorn src.api.server:app --reload

# In another terminal, watch tests
ptw -- tests/unit/
```

## Configuration

### Environment Variables

Create `.env` file with:

```bash
# Application
APP_NAME=model-serving-platform
APP_VERSION=1.0.0
LOG_LEVEL=INFO
ENVIRONMENT=development

# API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
API_TIMEOUT=30

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/models
DATABASE_POOL_SIZE=10

# Redis
REDIS_URL=redis://localhost:6379
REDIS_TTL=3600

# Model Storage
MODEL_STORAGE_TYPE=s3
MODEL_STORAGE_BUCKET=models
MODEL_STORAGE_ENDPOINT=http://localhost:9000
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin

# Vault
VAULT_ADDR=http://localhost:8200
VAULT_TOKEN=your-vault-token
VAULT_NAMESPACE=model-serving

# Monitoring
PROMETHEUS_ENABLED=true
PROMETHEUS_PORT=9090
JAEGER_ENABLED=true
JAEGER_ENDPOINT=http://localhost:14268/api/traces

# Security
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600
ENABLE_CORS=true
CORS_ORIGINS=["http://localhost:3000"]

# Feature Flags
ENABLE_CACHING=true
ENABLE_BATCH_PREDICTION=true
ENABLE_MODEL_VERSIONING=true
ENABLE_DRIFT_DETECTION=true
```

### Model Configuration

Edit `config/models.yaml`:

```yaml
models:
  - name: resnet50
    version: "1.0"
    framework: onnx
    path: s3://models/resnet50/model.onnx
    input_shape: [1, 3, 224, 224]
    batch_size: 32
    timeout: 100

  - name: bert-classifier
    version: "2.0"
    framework: onnx
    path: s3://models/bert/model.onnx
    max_sequence_length: 512
    batch_size: 16
    timeout: 200
```

## Monitoring and Debugging

### Accessing Dashboards

```bash
# Grafana
kubectl port-forward svc/prometheus-grafana 3000:80
# Open: http://localhost:3000
# Default credentials: admin/prom-operator

# Prometheus
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090
# Open: http://localhost:9090

# Jaeger
kubectl port-forward svc/jaeger-query 16686:16686
# Open: http://localhost:16686
```

### Viewing Logs

```bash
# Application logs
kubectl logs -f deployment/model-server

# All pods
kubectl logs -f -l app=model-server

# Previous instance
kubectl logs -p deployment/model-server

# Stream logs
stern model-server
```

### Metrics

```bash
# Application metrics
curl http://localhost:8000/metrics

# Query Prometheus
curl 'http://localhost:9090/api/v1/query?query=up'

# Check HPA metrics
kubectl get hpa model-server -o yaml
```

## Load Testing

### Using Locust

```bash
# Start Locust UI
locust -f tests/load/locustfile.py --host=http://localhost:8000

# Open: http://localhost:8089
# Configure users and spawn rate

# Headless mode
locust -f tests/load/locustfile.py \
  --host=http://localhost:8000 \
  --users 100 \
  --spawn-rate 10 \
  --run-time 10m \
  --headless
```

### Using K6

```bash
# Run K6 load test
k6 run tests/load/k6-script.js

# With options
k6 run tests/load/k6-script.js \
  --vus 100 \
  --duration 5m \
  --out json=results.json
```

## Troubleshooting

### Common Issues

#### Pod Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check resource quotas
kubectl describe resourcequota
```

#### Database Connection Issues

```bash
# Test database connection
kubectl run -it --rm debug --image=postgres:15 --restart=Never -- \
  psql -h postgresql -U user -d models

# Check database logs
kubectl logs -f postgresql-0
```

#### Model Loading Failures

```bash
# Check model storage access
kubectl exec -it <pod-name> -- \
  python -c "import boto3; print(boto3.client('s3').list_buckets())"

# Verify model files
kubectl exec -it <pod-name> -- ls -lh /models/
```

#### High Latency

```bash
# Check resource utilization
kubectl top pods

# Check HPA status
kubectl get hpa

# View traces in Jaeger
# Identify slow operations
```

### Debug Mode

```bash
# Enable debug logging
kubectl set env deployment/model-server LOG_LEVEL=DEBUG

# Attach debugger
kubectl port-forward <pod-name> 5678:5678
# Connect with VS Code or PyCharm
```

## API Documentation

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Next Steps

1. **Review Architecture**: Read [ARCHITECTURE.md](./ARCHITECTURE.md)
2. **Understand Requirements**: Check [REQUIREMENTS.md](./REQUIREMENTS.md)
3. **Implement Components**: Start with TODOs in source files
4. **Run Validation**: Follow [VALIDATION.md](./VALIDATION.md)
5. **Deploy to Production**: See [docs/OPERATIONS.md](./docs/OPERATIONS.md)

## Learning Resources

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- [Prometheus Guide](https://prometheus.io/docs/introduction/overview/)
- [ONNX Runtime Docs](https://onnxruntime.ai/docs/)
- [HashiCorp Vault Guide](https://learn.hashicorp.com/vault)

## Getting Help

- Check documentation in `docs/` directory
- Review code comments and TODOs
- Check runbooks in `docs/runbooks/`
- Search issues in the main repository

## Clean Up

### Local Development

```bash
# Stop application
# Ctrl+C in terminal running uvicorn

# Stop Docker services
docker-compose down

# Remove data volumes (optional)
docker-compose down -v
```

### Kubernetes

```bash
# Delete application
kubectl delete -f infrastructure/kubernetes/

# Delete Helm releases
helm uninstall prometheus vault postgresql redis

# Delete namespace
kubectl delete namespace model-serving

# Stop cluster
minikube stop  # or: kind delete cluster
```
