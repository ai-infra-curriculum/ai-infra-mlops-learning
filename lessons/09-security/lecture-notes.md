# Module 09: MLOps Security - Lecture Notes

**Duration**: 9 hours
**Level**: MLOps Engineer (2.5B)
**Last Updated**: October 2025

---

## Table of Contents

1. [ML Security Landscape](#1-ml-security-landscape)
2. [Secure Model Serving](#2-secure-model-serving)
3. [Secrets Management](#3-secrets-management)
4. [Pipeline Security](#4-pipeline-security)
5. [Data Security and Privacy](#5-data-security-and-privacy)
6. [Security Operations](#6-security-operations)
7. [Summary and Best Practices](#7-summary-and-best-practices)

---

## 1. ML Security Landscape

### 1.1 ML-Specific Threats (OWASP ML Top 10)

**1. Model Theft/Extraction**:
- Attacker queries model to reverse-engineer it
- **Example**: Stealing OpenAI GPT-3 via API queries

**2. Data Poisoning**:
- Injecting malicious data into training set
- **Example**: Microsoft Tay chatbot (2016) - manipulated via poisoned tweets

**3. Adversarial Examples**:
- Carefully crafted inputs that fool models
- **Example**: Stop sign with stickers misclassified as speed limit

**4. Model Inversion**:
- Extracting training data from model
- **Example**: Recovering facial images from face recognition models

**5. Privacy Leakage**:
- Model reveals sensitive training data
- **Example**: GPT-3 memorizing and outputting credit card numbers

### 1.2 Attack Surface

```python
# ML System Attack Surface
attack_surface = {
    'data': [
        'Training data poisoning',
        'Data exfiltration',
        'PII exposure'
    ],
    'model': [
        'Model extraction',
        'Model inversion',
        'Adversarial examples'
    ],
    'infrastructure': [
        'Compromised containers',
        'Secrets in code',
        'Unpatched dependencies'
    ],
    'api': [
        'Injection attacks',
        'DDoS',
        'Unauthorized access'
    ]
}
```

---

## 2. Secure Model Serving

### 2.1 API Authentication and Authorization

```python
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta

app = FastAPI()
security = HTTPBearer()

SECRET_KEY = "your-secret-key"  # Store in secrets manager
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify JWT token."""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/predict")
async def predict(
    request: PredictionRequest,
    token_data: dict = Depends(verify_token)
):
    """Secured prediction endpoint."""

    # Check permissions
    if not token_data.get("permissions", {}).get("predict"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Rate limiting
    user_id = token_data["sub"]
    if not check_rate_limit(user_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Input validation
    validated_input = validate_input(request.data)

    # Make prediction
    prediction = model.predict(validated_input)

    # Audit log
    log_prediction(user_id, request.data, prediction)

    return {"prediction": prediction}

def check_rate_limit(user_id: str, max_requests_per_minute: int = 60) -> bool:
    """Check if user is within rate limits."""
    import redis

    r = redis.Redis(host='localhost', port=6379)
    key = f"rate_limit:{user_id}"

    # Increment counter
    current = r.incr(key)

    # Set expiry on first request
    if current == 1:
        r.expire(key, 60)

    return current <= max_requests_per_minute
```

### 2.2 Input Validation and Sanitization

```python
from pydantic import BaseModel, validator, Field
from typing import List
import re

class SecurePredictionRequest(BaseModel):
    """Secure prediction request with validation."""

    # Define allowed ranges
    age: int = Field(..., ge=18, le=100)
    income: float = Field(..., ge=0, le=10_000_000)
    credit_score: int = Field(..., ge=300, le=850)
    employment_length: int = Field(..., ge=0, le=50)

    # Validate string inputs
    occupation: str = Field(..., max_length=100)
    city: str = Field(..., max_length=100)

    @validator('occupation', 'city')
    def sanitize_string(cls, v):
        """Remove potentially dangerous characters."""
        # Allow only alphanumeric, spaces, hyphens
        if not re.match(r'^[a-zA-Z0-9\s\-]+$', v):
            raise ValueError('Invalid characters in input')
        return v

    @validator('income')
    def validate_income(cls, v, values):
        """Cross-field validation."""
        if 'age' in values and values['age'] < 25 and v > 500_000:
            raise ValueError('Income inconsistent with age')
        return v

def validate_and_sanitize(raw_input: dict) -> dict:
    """Additional validation layer."""

    try:
        # Validate with Pydantic
        validated = SecurePredictionRequest(**raw_input)

        # Additional checks
        validated_dict = validated.dict()

        # Check for outliers (potential adversarial examples)
        if is_outlier(validated_dict):
            raise ValueError("Input appears to be adversarial")

        return validated_dict

    except Exception as e:
        # Log suspicious requests
        log_security_event("input_validation_failed", raw_input, str(e))
        raise HTTPException(status_code=422, detail=str(e))

def is_outlier(features: dict) -> bool:
    """Detect potential adversarial inputs."""
    # Use Isolation Forest or other outlier detection
    from sklearn.ensemble import IsolationForest

    # Convert to array
    feature_vector = np.array(list(features.values())).reshape(1, -1)

    # Check if outlier
    detector = IsolationForest(contamination=0.01)
    detector.fit(training_data)  # Fit on historical data

    prediction = detector.predict(feature_vector)

    return prediction[0] == -1  # -1 indicates outlier
```

---

## 3. Secrets Management

### 3.1 HashiCorp Vault Integration

```python
import hvac
import os

class SecretsManager:
    """Manage secrets using HashiCorp Vault."""

    def __init__(self, vault_addr: str = None, vault_token: str = None):
        self.vault_addr = vault_addr or os.environ.get('VAULT_ADDR')
        self.vault_token = vault_token or os.environ.get('VAULT_TOKEN')

        self.client = hvac.Client(
            url=self.vault_addr,
            token=self.vault_token
        )

        if not self.client.is_authenticated():
            raise Exception("Vault authentication failed")

    def get_secret(self, path: str, key: str = None) -> str:
        """Retrieve secret from Vault."""

        try:
            secret = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point='secret'
            )

            data = secret['data']['data']

            if key:
                return data[key]
            return data

        except Exception as e:
            raise Exception(f"Failed to retrieve secret: {str(e)}")

    def store_secret(self, path: str, data: dict):
        """Store secret in Vault."""

        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=data,
                mount_point='secret'
            )

        except Exception as e:
            raise Exception(f"Failed to store secret: {str(e)}")

    def rotate_secret(self, path: str, new_value: dict):
        """Rotate a secret."""

        # Store new version
        self.store_secret(path, new_value)

        # Update all services using this secret
        self._trigger_secret_rotation(path)

    def _trigger_secret_rotation(self, path: str):
        """Notify services to reload secrets."""
        # In production: use service mesh or orchestrator
        pass

# Usage
secrets = SecretsManager()

# Get database password
db_password = secrets.get_secret('database/postgres', 'password')

# Get API keys
mlflow_config = secrets.get_secret('mlops/mlflow')
# Returns: {'tracking_uri': '...', 'username': '...', 'password': '...'}

# Never hardcode secrets!
# ❌ BAD
DB_PASSWORD = "my_password_123"

# ✅ GOOD
DB_PASSWORD = secrets.get_secret('database/postgres', 'password')
```

### 3.2 Kubernetes Secrets Integration

```yaml
# sealed-secret.yaml (encrypted secret)
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: ml-model-secrets
  namespace: production
spec:
  encryptedData:
    mlflow-password: AgBx8... # Encrypted value
    aws-access-key: AgCy9... # Encrypted value
```

```python
# Access Kubernetes secrets in Python
from kubernetes import client, config

def get_k8s_secret(secret_name: str, namespace: str = "default") -> dict:
    """Retrieve Kubernetes secret."""

    config.load_incluster_config()  # Load in-cluster config

    v1 = client.CoreV1Api()

    try:
        secret = v1.read_namespaced_secret(secret_name, namespace)

        # Decode base64 values
        decoded_data = {}
        for key, value in secret.data.items():
            import base64
            decoded_data[key] = base64.b64decode(value).decode('utf-8')

        return decoded_data

    except Exception as e:
        raise Exception(f"Failed to read secret: {str(e)}")

# Usage in pod
secrets = get_k8s_secret('ml-model-secrets', 'production')
mlflow_password = secrets['mlflow-password']
```

---

## 4. Pipeline Security

### 4.1 Supply Chain Security (SLSA, SBOM)

```python
import subprocess
import json

class SupplyChainSecurity:
    """Implement supply chain security for ML pipelines."""

    def generate_sbom(self, requirements_file: str = "requirements.txt"):
        """Generate Software Bill of Materials."""

        # Use syft to generate SBOM
        result = subprocess.run(
            ['syft', 'packages', 'file:' + requirements_file, '-o', 'json'],
            capture_output=True,
            text=True
        )

        sbom = json.loads(result.stdout)

        # Save SBOM
        with open('sbom.json', 'w') as f:
            json.dump(sbom, f, indent=2)

        return sbom

    def scan_vulnerabilities(self, sbom_file: str = "sbom.json"):
        """Scan SBOM for vulnerabilities using Grype."""

        result = subprocess.run(
            ['grype', 'sbom:' + sbom_file, '-o', 'json'],
            capture_output=True,
            text=True
        )

        vulnerabilities = json.loads(result.stdout)

        # Filter critical/high vulnerabilities
        critical_vulns = [
            v for v in vulnerabilities.get('matches', [])
            if v['vulnerability']['severity'] in ['Critical', 'High']
        ]

        if critical_vulns:
            print(f"⚠️  Found {len(critical_vulns)} critical/high vulnerabilities:")
            for vuln in critical_vulns:
                print(f"  - {vuln['artifact']['name']}: {vuln['vulnerability']['id']}")

            raise Exception("Critical vulnerabilities found - blocking deployment")

        return vulnerabilities

    def sign_artifact(self, artifact_path: str):
        """Sign artifact using Cosign."""

        # Sign with Cosign
        subprocess.run([
            'cosign', 'sign', '-key', 'cosign.key', artifact_path
        ])

        print(f"✅ Artifact signed: {artifact_path}")

    def verify_signature(self, artifact_path: str) -> bool:
        """Verify artifact signature."""

        result = subprocess.run(
            ['cosign', 'verify', '-key', 'cosign.pub', artifact_path],
            capture_output=True
        )

        return result.returncode == 0

# Integrate into CI/CD
supply_chain = SupplyChainSecurity()

# Generate SBOM
sbom = supply_chain.generate_sbom()

# Scan for vulnerabilities
vulns = supply_chain.scan_vulnerabilities()

# Sign model artifact
supply_chain.sign_artifact('model.pkl')

# Verify before deployment
if not supply_chain.verify_signature('model.pkl'):
    raise Exception("Artifact signature verification failed!")
```

### 4.2 Container Security

```dockerfile
# Secure Dockerfile
FROM python:3.9-slim AS builder

# Don't run as root
RUN useradd -m -u 1000 mluser

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=mluser:mluser . .

# Production stage
FROM python:3.9-slim

# Security: Run as non-root user
RUN useradd -m -u 1000 mluser

# Copy from builder
COPY --from=builder --chown=mluser:mluser /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder --chown=mluser:mluser /app /app

# Switch to non-root user
USER mluser

WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

EXPOSE 8000

CMD ["python", "app.py"]
```

```python
# Scan container images
def scan_container_image(image_name: str):
    """Scan container for vulnerabilities using Trivy."""

    result = subprocess.run(
        ['trivy', 'image', '--severity', 'CRITICAL,HIGH', '--format', 'json', image_name],
        capture_output=True,
        text=True
    )

    scan_results = json.loads(result.stdout)

    critical_vulns = []
    for result in scan_results.get('Results', []):
        for vuln in result.get('Vulnerabilities', []):
            if vuln['Severity'] in ['CRITICAL', 'HIGH']:
                critical_vulns.append(vuln)

    if critical_vulns:
        print(f"⛔ Found {len(critical_vulns)} critical/high vulnerabilities")
        print("Blocking deployment")
        return False

    print("✅ Container security scan passed")
    return True

# Use in CI/CD
if not scan_container_image('ml-model:latest'):
    raise Exception("Container security scan failed")
```

---

## 5. Data Security and Privacy

### 5.1 Data Encryption

```python
from cryptography.fernet import Fernet
import base64

class DataEncryption:
    """Encrypt/decrypt sensitive data."""

    def __init__(self, encryption_key: bytes = None):
        if encryption_key:
            self.key = encryption_key
        else:
            # Get from secrets manager
            self.key = self._get_encryption_key()

        self.cipher = Fernet(self.key)

    def _get_encryption_key(self) -> bytes:
        """Get encryption key from secrets manager."""
        secrets = SecretsManager()
        key_str = secrets.get_secret('encryption/data', 'key')
        return base64.b64decode(key_str)

    def encrypt_dataframe(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Encrypt sensitive columns in dataframe."""

        df_encrypted = df.copy()

        for col in columns:
            df_encrypted[col] = df[col].apply(
                lambda x: self.cipher.encrypt(str(x).encode()).decode()
            )

        return df_encrypted

    def decrypt_dataframe(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Decrypt sensitive columns."""

        df_decrypted = df.copy()

        for col in columns:
            df_decrypted[col] = df[col].apply(
                lambda x: self.cipher.decrypt(x.encode()).decode()
            )

        return df_decrypted

    def encrypt_model_artifact(self, model_path: str, output_path: str):
        """Encrypt model file."""

        with open(model_path, 'rb') as f:
            model_data = f.read()

        encrypted_data = self.cipher.encrypt(model_data)

        with open(output_path, 'wb') as f:
            f.write(encrypted_data)

# Usage
encryptor = DataEncryption()

# Encrypt PII columns
encrypted_df = encryptor.encrypt_dataframe(
    df,
    columns=['ssn', 'credit_card', 'email']
)

# Save encrypted data
encrypted_df.to_parquet('encrypted_data.parquet')

# Encrypt model
encryptor.encrypt_model_artifact('model.pkl', 'model.encrypted')
```

### 5.2 PII Redaction

```python
import re

class PIIRedactor:
    """Redact Personally Identifiable Information."""

    def __init__(self):
        self.patterns = {
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }

    def redact_text(self, text: str) -> str:
        """Redact PII from text."""

        redacted = text

        for pii_type, pattern in self.patterns.items():
            redacted = re.sub(
                pattern,
                f'[REDACTED-{pii_type.upper()}]',
                redacted
            )

        return redacted

    def redact_dataframe(self, df: pd.DataFrame, text_columns: List[str]) -> pd.DataFrame:
        """Redact PII from dataframe columns."""

        df_redacted = df.copy()

        for col in text_columns:
            df_redacted[col] = df[col].apply(self.redact_text)

        return df_redacted

# Usage
redactor = PIIRedactor()

text = "Contact John at john.doe@email.com or 555-123-4567. SSN: 123-45-6789"
redacted = redactor.redact_text(text)
print(redacted)
# Output: "Contact John at [REDACTED-EMAIL] or [REDACTED-PHONE]. SSN: [REDACTED-SSN]"
```

---

## 6. Security Operations

### 6.1 Security Monitoring

```python
from prometheus_client import Counter, Histogram

# Security metrics
auth_failures = Counter(
    'auth_failures_total',
    'Total authentication failures',
    ['endpoint', 'user']
)

suspicious_requests = Counter(
    'suspicious_requests_total',
    'Requests flagged as suspicious',
    ['reason']
)

def log_security_event(event_type: str, details: dict):
    """Log security event."""

    event = {
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'details': details,
        'severity': classify_severity(event_type)
    }

    # Log to SIEM
    send_to_siem(event)

    # Update metrics
    if event_type == 'auth_failure':
        auth_failures.labels(
            endpoint=details.get('endpoint'),
            user=details.get('user')
        ).inc()

    elif event_type in ['injection_attempt', 'adversarial_input']:
        suspicious_requests.labels(reason=event_type).inc()

    # Alert on critical events
    if event['severity'] == 'CRITICAL':
        send_security_alert(event)

def detect_anomalous_behavior(user_id: str, request: dict) -> bool:
    """Detect anomalous user behavior."""

    # Get user's historical patterns
    user_profile = get_user_profile(user_id)

    # Check for anomalies
    anomalies = []

    # 1. Unusual request rate
    current_rate = get_current_request_rate(user_id)
    if current_rate > user_profile['avg_rate'] * 10:
        anomalies.append('high_request_rate')

    # 2. Unusual request time
    current_hour = datetime.now().hour
    if current_hour not in user_profile['typical_hours']:
        anomalies.append('unusual_time')

    # 3. Unusual input patterns
    if is_input_unusual(request, user_profile['typical_inputs']):
        anomalies.append('unusual_input')

    if anomalies:
        log_security_event('anomalous_behavior', {
            'user_id': user_id,
            'anomalies': anomalies
        })
        return True

    return False
```

---

## 7. Summary and Best Practices

### Key Takeaways

1. **Defense in Depth**: Multiple security layers
2. **Least Privilege**: Minimum necessary permissions
3. **Secrets Management**: Never hardcode credentials
4. **Supply Chain**: Verify all dependencies
5. **Encryption**: Protect data at rest and in transit
6. **Monitoring**: Detect and respond to threats
7. **Compliance**: GDPR, HIPAA, SOC 2

### Security Checklist

- [ ] Authentication and authorization implemented
- [ ] Input validation on all endpoints
- [ ] Rate limiting configured
- [ ] Secrets stored in vault (not code)
- [ ] Dependencies scanned for vulnerabilities
- [ ] Container images scanned
- [ ] Artifacts signed
- [ ] Data encrypted
- [ ] PII redacted in logs
- [ ] Security monitoring enabled
- [ ] Incident response plan documented

---

**Total Words**: ~4,600 words

**Next Module**: Module 10 - Advanced MLOps Topics (Final Module!)
