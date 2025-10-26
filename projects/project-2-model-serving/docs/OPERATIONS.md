# Operations Guide

## Deployment

### Prerequisites
- Kubernetes cluster (1.24+)
- kubectl configured
- Helm 3.0+
- Docker registry access

### Deploy to Production

```bash
# 1. Create namespace
kubectl create namespace model-serving

# 2. Create secrets
kubectl create secret generic model-server-secrets \
  --from-literal=database-url=<database-url> \
  --from-literal=redis-url=<redis-url> \
  --namespace model-serving

# 3. Deploy infrastructure
helm install prometheus prometheus-community/kube-prometheus-stack \
  -f infrastructure/prometheus/values.yaml \
  --namespace model-serving

helm install vault hashicorp/vault \
  -f infrastructure/vault/values.yaml \
  --namespace model-serving

# 4. Deploy application
kubectl apply -f infrastructure/kubernetes/

# 5. Verify deployment
kubectl get pods -n model-serving
kubectl get svc -n model-serving
```

## Monitoring

### Access Dashboards

```bash
# Grafana
kubectl port-forward svc/prometheus-grafana 3000:80 -n model-serving
# Open: http://localhost:3000

# Prometheus
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n model-serving
# Open: http://localhost:9090
```

### Key Metrics to Monitor

1. **Request Rate**
   - Metric: `http_requests_total`
   - Alert: Sudden drops or spikes

2. **Latency**
   - Metrics: `http_request_duration_seconds_bucket`
   - Alert: P95 > 100ms, P99 > 200ms

3. **Error Rate**
   - Metric: `http_requests_total{status=~"5.."}`
   - Alert: > 0.1%

4. **Model Performance**
   - Metrics: `model_prediction_duration_seconds`
   - Alert: Degradation over time

5. **Resource Usage**
   - Metrics: CPU, memory utilization
   - Alert: > 90%

## Scaling

### Manual Scaling

```bash
# Scale deployment
kubectl scale deployment model-server --replicas=10 -n model-serving

# Verify scaling
kubectl get hpa -n model-serving
```

### Auto-Scaling

HPA is configured to scale based on:
- CPU utilization (70% threshold)
- Memory utilization (80% threshold)
- Custom metrics (requests/second, latency)

Monitor HPA:
```bash
kubectl get hpa model-server-hpa -n model-serving -w
```

## Incident Response

### Common Issues

#### 1. High Latency

**Symptoms**: P95/P99 latency above thresholds

**Diagnosis**:
```bash
# Check pod resources
kubectl top pods -n model-serving

# Check HPA status
kubectl get hpa -n model-serving

# View logs
kubectl logs -f deployment/model-server -n model-serving
```

**Resolution**:
- Scale up if resource-constrained
- Check for slow model inference
- Review database query performance

#### 2. High Error Rate

**Symptoms**: Increased 5xx errors

**Diagnosis**:
```bash
# View application logs
kubectl logs -f deployment/model-server -n model-serving | grep ERROR

# Check pod status
kubectl get pods -n model-serving

# Describe failing pods
kubectl describe pod <pod-name> -n model-serving
```

**Resolution**:
- Review error logs
- Check external dependencies (database, Redis)
- Rollback if recent deployment caused issues

#### 3. Model Loading Failures

**Symptoms**: Models fail to load

**Diagnosis**:
```bash
# Check logs
kubectl logs -f deployment/model-server -n model-serving

# Verify S3 access
kubectl exec -it <pod-name> -n model-serving -- \
  aws s3 ls s3://models/

# Check vault secrets
kubectl exec -it <pod-name> -n model-serving -- \
  vault kv get secret/database
```

**Resolution**:
- Verify S3 credentials
- Check model file integrity
- Ensure sufficient disk space

### Runbooks

#### Rollback Deployment

```bash
# View rollout history
kubectl rollout history deployment/model-server -n model-serving

# Rollback to previous version
kubectl rollout undo deployment/model-server -n model-serving

# Rollback to specific revision
kubectl rollout undo deployment/model-server --to-revision=3 -n model-serving
```

#### Restart Pods

```bash
# Restart all pods
kubectl rollout restart deployment/model-server -n model-serving

# Delete specific pod (will be recreated)
kubectl delete pod <pod-name> -n model-serving
```

#### Update Configuration

```bash
# Edit ConfigMap
kubectl edit configmap model-server-config -n model-serving

# Restart to pick up changes
kubectl rollout restart deployment/model-server -n model-serving
```

## Maintenance

### Database Maintenance

```bash
# Backup database
kubectl exec -it postgresql-0 -n model-serving -- \
  pg_dump -U user models > backup.sql

# Restore database
kubectl exec -i postgresql-0 -n model-serving -- \
  psql -U user models < backup.sql
```

### Log Management

```bash
# View logs
kubectl logs -f deployment/model-server -n model-serving

# View logs from all replicas
kubectl logs -f -l app=model-server -n model-serving

# Export logs
kubectl logs deployment/model-server -n model-serving > logs.txt
```

### Certificate Renewal

```bash
# Check certificate expiration
kubectl get certificate -n model-serving

# Force renewal
kubectl delete certificate model-server-tls -n model-serving
# cert-manager will recreate it
```

## Security

### Rotate Secrets

```bash
# Generate new secret
kubectl create secret generic model-server-secrets-new \
  --from-literal=database-url=<new-url> \
  --namespace model-serving

# Update deployment
kubectl set env deployment/model-server \
  --from=secret/model-server-secrets-new \
  --namespace model-serving

# Delete old secret
kubectl delete secret model-server-secrets -n model-serving
```

### Audit Logs

```bash
# View audit logs
kubectl logs -f deployment/model-server -n model-serving | grep AUDIT
```

## Performance Tuning

### Resource Optimization

1. **CPU**: Adjust based on model complexity
2. **Memory**: Monitor for memory leaks
3. **Replicas**: Based on traffic patterns

### Model Optimization

1. **Model Quantization**: Reduce model size
2. **Batch Processing**: Increase throughput
3. **Caching**: Cache frequent predictions

## Disaster Recovery

### Backup Procedures

1. **Database**: Daily automated backups
2. **Models**: S3 versioning enabled
3. **Configuration**: Git repository

### Recovery Procedures

1. **Database Restore**: From latest backup
2. **Redeploy Application**: From Git
3. **Reload Models**: From S3

## Contacts

- **On-Call Engineer**: pagerduty.com/model-serving
- **Team Slack**: #model-serving
- **Email**: model-serving@example.com
