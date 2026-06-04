## Exercise 4: Build a Minimal MLOps Stack with Free Tools (120 minutes)

**Objective**: Stand up the smallest end-to-end MLOps stack possible using only OSS tools.

### Background

You're a 2-person team that just shipped your first model. You need
fundamentals NOW without procuring vendor tools. The minimal "real" stack:
- MLflow tracking server (local)
- DVC (data + model versioning)
- A simple FastAPI serving wrapper
- Prometheus + Grafana for monitoring

### Tasks

1. Install everything locally:
   ```bash
   pip install mlflow dvc[s3] fastapi uvicorn prometheus-client
   ```

2. Run a training script that logs to MLflow.

3. Version the dataset + model in DVC with a local remote.

4. Wrap the trained model in FastAPI; expose `/predict` + `/metrics`.

5. Run Prometheus + Grafana locally (Docker compose).

6. Demonstrate the full loop:
   - retrain → MLflow run logged
   - new model version → DVC `dvc push`
   - new FastAPI deploy → request → metric in Grafana

### Deliverable

A working repo with: `train.py`, `dvc.yaml`, `app.py`, `docker-compose.yaml`,
`grafana-dashboard.json`, and `README.md` documenting the setup.

### Acceptance criteria

- All commands in README are copy-paste runnable
- Grafana shows live latency + RPS panels
- DVC tracks both the dataset and the model artifact

---
