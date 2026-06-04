# API Documentation

## Overview

The Model Serving Platform provides a RESTful API for model predictions, management, and monitoring.

Base URL: `http://localhost:8000` (development)

## Authentication

All endpoints (except health checks and docs) require authentication via JWT token.

```http
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### Health Checks

#### GET /health
Health check endpoint.

**Response**
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "vault": "connected",
  "models_loaded": 3
}
```

#### GET /ready
Readiness check for Kubernetes.

#### GET /live
Liveness check for Kubernetes.

### Predictions

#### POST /predict/{model_name}
Make a single prediction.

**Parameters**
- `model_name` (path): Name of the model

**Request Body**
```json
{
  "features": [1.0, 2.0, 3.0, 4.0],
  "model_version": "1.0.0"  // optional
}
```

**Response**
```json
{
  "prediction": 0.95,
  "confidence": 0.87,
  "model_name": "classifier",
  "model_version": "1.0.0",
  "latency_ms": 23.5
}
```

#### POST /predict/{model_name}/batch
Make batch predictions.

**Request Body**
```json
{
  "instances": [
    {"features": [1.0, 2.0, 3.0]},
    {"features": [4.0, 5.0, 6.0]}
  ],
  "max_workers": 4
}
```

### Model Management

#### GET /models
List all available models.

**Response**
```json
[
  {
    "name": "resnet50",
    "version": "1.0",
    "framework": "onnx",
    "description": "Image classification model",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "status": "active",
    "size_mb": 98.5
  }
]
```

#### GET /models/{model_name}
Get information about a specific model.

#### POST /models/register
Register a new model (admin only).

**Request Body**
```json
{
  "name": "new-model",
  "version": "1.0.0",
  "framework": "onnx",
  "path": "s3://models/new-model/model.onnx",
  "description": "New model description",
  "metadata": {
    "input_shape": [1, 3, 224, 224],
    "output_classes": 1000
  }
}
```

#### DELETE /models/{model_name}
Delete a model (admin only).

#### POST /models/{model_name}/load
Explicitly load a model into memory.

#### POST /models/{model_name}/unload
Unload a model from memory.

### Metrics

#### GET /metrics
Prometheus metrics endpoint.

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message",
  "type": "ValidationError",
  "errors": [
    {
      "loc": ["body", "features"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### HTTP Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service temporarily unavailable

## Rate Limiting

API requests are rate-limited:
- Default: 100 requests per minute per user
- Burst: 200 requests

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

## Interactive Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
