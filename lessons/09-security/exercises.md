# Module 09: MLOps Security - Exercises

## Overview

This exercise set provides hands-on practice with MLOps security concepts, including:
- ML threat modeling and OWASP ML Top 10
- Secrets management with HashiCorp Vault
- Supply chain security (SLSA, SBOM, Cosign)
- Container and runtime security
- Complete MLOps security framework

**Time Estimate**: 6-9 hours total

---

## Exercise 1: ML Threat Modeling & OWASP ML Top 10 (90 minutes)

**Objective**: Conduct comprehensive threat modeling for an ML system and implement defenses against OWASP ML Top 10 threats.

### Background

Your team is deploying a fraud detection model as a public API. You need to identify potential security threats and implement appropriate defenses.

### Tasks

1. **Conduct threat modeling using STRIDE framework**
2. **Identify OWASP ML Top 10 threats applicable to your system**
3. **Implement rate limiting to prevent model extraction**
4. **Add input validation to prevent adversarial attacks**
5. **Create security documentation and threat matrix**

### Starter Code

```python
# src/security/threat_model.py
"""ML Threat Modeling Framework."""

from typing import Dict, List, Set
from dataclasses import dataclass
from enum import Enum

class ThreatCategory(Enum):
    """STRIDE threat categories."""
    SPOOFING = "spoofing"
    TAMPERING = "tampering"
    REPUDIATION = "repudiation"
    INFORMATION_DISCLOSURE = "information_disclosure"
    DENIAL_OF_SERVICE = "denial_of_service"
    ELEVATION_OF_PRIVILEGE = "elevation_of_privilege"

class OWASPMLThreat(Enum):
    """OWASP ML Top 10 threats."""
    MODEL_THEFT = "model_theft"
    DATA_POISONING = "data_poisoning"
    ADVERSARIAL_EXAMPLES = "adversarial_examples"
    MODEL_INVERSION = "model_inversion"
    PRIVACY_LEAKAGE = "privacy_leakage"
    SUPPLY_CHAIN = "supply_chain"
    TRANSFER_LEARNING = "transfer_learning"
    OUTPUT_INTEGRITY = "output_integrity"
    NEURAL_NET_REPROGRAMMING = "neural_net_reprogramming"
    ABUSE_ML_SYSTEM = "abuse_ml_system"

@dataclass
class Threat:
    """Security threat definition."""
    id: str
    name: str
    category: ThreatCategory
    owasp_ml: OWASPMLThreat
    description: str
    impact: str  # "low", "medium", "high", "critical"
    likelihood: str  # "low", "medium", "high"
    affected_components: List[str]
    mitigations: List[str]

    def risk_score(self) -> int:
        """Calculate risk score (impact * likelihood)."""
        # TODO: Implement risk scoring
        # Impact: low=1, medium=2, high=3, critical=4
        # Likelihood: low=1, medium=2, high=3
        # Return: impact_score * likelihood_score
        pass

class ThreatModel:
    """ML system threat model."""

    def __init__(self, system_name: str):
        """
        Initialize threat model.

        Args:
            system_name: Name of ML system being modeled
        """
        self.system_name = system_name
        self.threats: List[Threat] = []
        self.assets: List[str] = []
        self.entry_points: List[str] = []

    def add_asset(self, asset: str):
        """Add system asset to protect."""
        # TODO: Add asset to list
        pass

    def add_entry_point(self, entry_point: str):
        """Add system entry point (attack surface)."""
        # TODO: Add entry point to list
        pass

    def add_threat(self, threat: Threat):
        """Add identified threat."""
        # TODO: Add threat to list
        pass

    def analyze_stride(self) -> Dict[ThreatCategory, List[Threat]]:
        """
        Analyze threats using STRIDE framework.

        Returns:
            Dictionary mapping STRIDE categories to threats
        """
        # TODO: Group threats by STRIDE category
        # TODO: Return categorized threats
        pass

    def analyze_owasp_ml(self) -> Dict[OWASPMLThreat, List[Threat]]:
        """
        Analyze threats using OWASP ML Top 10.

        Returns:
            Dictionary mapping OWASP ML threats to identified threats
        """
        # TODO: Group threats by OWASP ML category
        # TODO: Return categorized threats
        pass

    def prioritize_threats(self) -> List[Threat]:
        """
        Prioritize threats by risk score.

        Returns:
            Sorted list of threats (highest risk first)
        """
        # TODO: Calculate risk score for each threat
        # TODO: Sort by risk score descending
        # TODO: Return prioritized list
        pass

    def generate_threat_matrix(self) -> str:
        """
        Generate threat matrix document.

        Returns:
            Markdown formatted threat matrix
        """
        # TODO: Create markdown table with:
        #   - Threat name
        #   - Category
        #   - Impact
        #   - Likelihood
        #   - Risk score
        #   - Mitigations
        # TODO: Group by risk level
        # TODO: Include summary statistics
        pass

    def export_to_json(self, filepath: str):
        """Export threat model to JSON."""
        # TODO: Serialize threat model
        # TODO: Save to file
        pass

# Defense implementations

from fastapi import FastAPI, HTTPException, Request
from fastapi.security import APIKeyHeader
import time
from collections import defaultdict
import hashlib

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key")

class RateLimiter:
    """Rate limiter to prevent model extraction attacks."""

    def __init__(self, max_requests: int, window_seconds: int):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum requests per window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """
        Check if request is allowed.

        Args:
            client_id: Unique client identifier

        Returns:
            True if allowed, False if rate limit exceeded
        """
        # TODO: Get current timestamp
        # TODO: Remove old requests outside window
        # TODO: Check if under limit
        # TODO: Add current request if allowed
        # TODO: Return result
        pass

    def get_client_id(self, request: Request) -> str:
        """Get unique client identifier from request."""
        # TODO: Extract IP address
        # TODO: Optionally include API key
        # TODO: Hash for privacy
        # TODO: Return client ID
        pass

class InputValidator:
    """Input validator to prevent adversarial attacks."""

    def __init__(self, feature_ranges: Dict[str, tuple]):
        """
        Initialize input validator.

        Args:
            feature_ranges: Dict mapping feature names to (min, max) tuples
        """
        self.feature_ranges = feature_ranges

    def validate(self, input_data: Dict) -> bool:
        """
        Validate input data.

        Args:
            input_data: Input features

        Returns:
            True if valid, False otherwise
        """
        # TODO: Check all required features present
        # TODO: Validate each feature in acceptable range
        # TODO: Check for suspicious patterns (e.g., all features at boundaries)
        # TODO: Validate data types
        # TODO: Return validation result
        pass

    def detect_adversarial(self, input_data: Dict, confidence: float) -> bool:
        """
        Detect potential adversarial examples.

        Args:
            input_data: Input features
            confidence: Model confidence score

        Returns:
            True if potentially adversarial, False otherwise
        """
        # TODO: Check for low confidence on edge case inputs
        # TODO: Compare to training distribution
        # TODO: Detect unusual feature combinations
        # TODO: Return detection result
        pass

# Example API with security controls

rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Apply rate limiting to all requests."""
    # TODO: Get client ID
    # TODO: Check rate limit
    # TODO: Raise HTTPException if exceeded
    # TODO: Otherwise, continue to endpoint
    pass

@app.post("/predict")
async def predict(
    request: Request,
    input_data: Dict,
    api_key: str = Security(api_key_header)
):
    """
    Secured prediction endpoint.

    Security controls:
    - API key authentication
    - Rate limiting
    - Input validation
    - Adversarial detection
    """
    # TODO: Validate API key
    # TODO: Validate input data
    # TODO: Make prediction
    # TODO: Check for adversarial patterns
    # TODO: Return prediction with confidence
    pass
```

### Example Threat Model

```python
# scripts/create_threat_model.py
"""Create threat model for fraud detection API."""

from src.security.threat_model import (
    ThreatModel, Threat, ThreatCategory, OWASPMLThreat
)

def create_fraud_detection_threat_model():
    """Create threat model for fraud detection system."""
    model = ThreatModel("Fraud Detection API")

    # Define assets
    # TODO: Add assets (model weights, training data, customer PII, etc.)

    # Define entry points
    # TODO: Add entry points (REST API, batch processing, admin panel, etc.)

    # Define threats
    # TODO: Add threat: Model extraction via API queries
    model_theft = Threat(
        id="T001",
        name="Model Extraction via API Queries",
        category=ThreatCategory.INFORMATION_DISCLOSURE,
        owasp_ml=OWASPMLThreat.MODEL_THEFT,
        description="Attacker queries API repeatedly to reverse-engineer model",
        impact="high",
        likelihood="medium",
        affected_components=["prediction_api", "model_weights"],
        mitigations=[
            "Implement rate limiting (100 req/hour per client)",
            "Add API key authentication",
            "Monitor for suspicious query patterns",
            "Add prediction output rounding to reduce information leakage"
        ]
    )
    model.add_threat(model_theft)

    # TODO: Add more threats for:
    #   - Data poisoning in feedback loop
    #   - Adversarial examples
    #   - Privacy leakage
    #   - DDoS attacks
    #   - Unauthorized access

    # Generate reports
    print("\n=== STRIDE Analysis ===")
    # TODO: Print STRIDE analysis

    print("\n=== OWASP ML Top 10 Analysis ===")
    # TODO: Print OWASP ML analysis

    print("\n=== Prioritized Threats ===")
    # TODO: Print prioritized threats

    # Export
    model.generate_threat_matrix()
    model.export_to_json("threat_model.json")

if __name__ == '__main__':
    create_fraud_detection_threat_model()
```

### Validation Tests

```python
# tests/test_threat_model.py
import pytest
from src.security.threat_model import (
    ThreatModel, Threat, ThreatCategory, OWASPMLThreat, RateLimiter, InputValidator
)

def test_risk_score_calculation():
    """Test risk score is calculated correctly."""
    threat = Threat(
        id="T001",
        name="Test Threat",
        category=ThreatCategory.SPOOFING,
        owasp_ml=OWASPMLThreat.MODEL_THEFT,
        description="Test",
        impact="high",  # 3
        likelihood="medium",  # 2
        affected_components=["api"],
        mitigations=[]
    )
    # TODO: Assert risk_score() == 6
    pass

def test_rate_limiter_allows_within_limit():
    """Test rate limiter allows requests within limit."""
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    client_id = "test_client"

    # TODO: Make 5 requests
    # TODO: Assert all allowed
    pass

def test_rate_limiter_blocks_over_limit():
    """Test rate limiter blocks requests over limit."""
    # TODO: Implement test
    pass

def test_input_validator_accepts_valid_input():
    """Test input validator accepts valid input."""
    validator = InputValidator({
        'amount': (0, 10000),
        'age': (18, 100)
    })

    valid_input = {'amount': 500, 'age': 35}
    # TODO: Assert validate returns True
    pass

def test_input_validator_rejects_out_of_range():
    """Test input validator rejects out of range input."""
    # TODO: Implement test
    pass

def test_threat_prioritization():
    """Test threats are prioritized by risk score."""
    # TODO: Create threat model with multiple threats
    # TODO: Add threats with different risk scores
    # TODO: Get prioritized list
    # TODO: Assert sorted by risk score descending
    pass
```

### Success Criteria

- [ ] Threat model identifies at least 8 threats from OWASP ML Top 10
- [ ] STRIDE analysis covers all six categories
- [ ] Risk scores are calculated correctly
- [ ] Rate limiter prevents model extraction (max 100 req/hour)
- [ ] Input validation catches out-of-range and adversarial inputs
- [ ] Threat matrix document is comprehensive and actionable
- [ ] Mitigations are specific and implementable

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **STRIDE Analysis**: For each component, ask:
   - Spoofing: Can attacker impersonate?
   - Tampering: Can data be modified?
   - Repudiation: Can actions be denied?
   - Information Disclosure: Can data leak?
   - Denial of Service: Can service be disrupted?
   - Elevation of Privilege: Can attacker gain higher access?

2. **Risk Score Formula**:
```python
impact_values = {"low": 1, "medium": 2, "high": 3, "critical": 4}
likelihood_values = {"low": 1, "medium": 2, "high": 3}
risk_score = impact_values[impact] * likelihood_values[likelihood]
```

3. **Rate Limiting**:
```python
current_time = time.time()
window_start = current_time - self.window_seconds
self.requests[client_id] = [
    req_time for req_time in self.requests[client_id]
    if req_time > window_start
]
return len(self.requests[client_id]) < self.max_requests
```

4. **Input Validation**: Check each feature against allowed range and detect statistical anomalies

5. **OWASP ML Top 10**: Focus on Model Theft, Adversarial Examples, Privacy Leakage for API scenarios

</details>

---

## Exercise 2: Secrets Management with HashiCorp Vault (90 minutes)

**Objective**: Implement secrets management using HashiCorp Vault for ML pipelines.

### Background

Your ML pipeline needs to access multiple secrets (database passwords, API keys, model signing keys). Implement HashiCorp Vault integration to securely manage these secrets.

### Tasks

1. **Set up HashiCorp Vault (dev mode)**
2. **Store ML pipeline secrets in Vault**
3. **Implement secrets rotation**
4. **Integrate with ML training and serving**
5. **Implement dynamic database credentials**

### Starter Code

```python
# src/security/secrets_manager.py
"""Secrets management with HashiCorp Vault."""

import hvac
from typing import Dict, Optional
import os
from dataclasses import dataclass

@dataclass
class SecretMetadata:
    """Metadata for a secret."""
    path: str
    version: int
    created_time: str

class VaultSecretsManager:
    """HashiCorp Vault secrets manager."""

    def __init__(
        self,
        vault_url: str = "http://localhost:8200",
        token: Optional[str] = None
    ):
        """
        Initialize Vault client.

        Args:
            vault_url: Vault server URL
            token: Vault token (if None, uses VAULT_TOKEN env var)
        """
        # TODO: Initialize hvac client
        # TODO: Use token from parameter or environment
        # TODO: Verify client is authenticated
        self.client = None
        pass

    def store_secret(
        self,
        path: str,
        secret_data: Dict,
        mount_point: str = "secret"
    ) -> SecretMetadata:
        """
        Store secret in Vault.

        Args:
            path: Secret path (e.g., "mlops/db-password")
            secret_data: Secret key-value pairs
            mount_point: Vault mount point

        Returns:
            Secret metadata
        """
        # TODO: Store secret using KV v2 engine
        # TODO: Return metadata
        pass

    def get_secret(
        self,
        path: str,
        version: Optional[int] = None,
        mount_point: str = "secret"
    ) -> Dict:
        """
        Retrieve secret from Vault.

        Args:
            path: Secret path
            version: Specific version (None = latest)
            mount_point: Vault mount point

        Returns:
            Secret data dictionary
        """
        # TODO: Read secret from Vault
        # TODO: Handle version parameter
        # TODO: Return secret data
        pass

    def rotate_secret(self, path: str, new_secret_data: Dict) -> SecretMetadata:
        """
        Rotate secret (create new version).

        Args:
            path: Secret path
            new_secret_data: New secret data

        Returns:
            New secret metadata
        """
        # TODO: Store new version of secret
        # TODO: Old version remains accessible
        # TODO: Return new metadata
        pass

    def delete_secret(self, path: str, versions: List[int] = None):
        """
        Delete secret versions.

        Args:
            path: Secret path
            versions: Versions to delete (None = all)
        """
        # TODO: Delete specified versions
        # TODO: If versions is None, delete all
        pass

    def create_db_credentials(
        self,
        db_name: str,
        role: str,
        ttl: str = "1h"
    ) -> Dict:
        """
        Create dynamic database credentials.

        Args:
            db_name: Database name
            role: Vault database role
            ttl: Credential TTL (e.g., "1h", "24h")

        Returns:
            Temporary database credentials
        """
        # TODO: Request dynamic credentials from Vault database engine
        # TODO: Credentials automatically expire after TTL
        # TODO: Return username and password
        pass

    def renew_lease(self, lease_id: str, increment: str = "1h"):
        """
        Renew a lease.

        Args:
            lease_id: Lease ID to renew
            increment: Renewal increment
        """
        # TODO: Renew lease
        pass

    def revoke_lease(self, lease_id: str):
        """
        Revoke a lease.

        Args:
            lease_id: Lease ID to revoke
        """
        # TODO: Revoke lease immediately
        pass

# ML Pipeline integration

class MLPipelineSecrets:
    """Secrets for ML pipeline."""

    def __init__(self, vault_manager: VaultSecretsManager):
        """
        Initialize with Vault manager.

        Args:
            vault_manager: VaultSecretsManager instance
        """
        self.vault = vault_manager

    def get_mlflow_credentials(self) -> Dict:
        """Get MLflow tracking server credentials."""
        # TODO: Retrieve from Vault path "mlops/mlflow"
        pass

    def get_s3_credentials(self) -> Dict:
        """Get S3 credentials for model storage."""
        # TODO: Retrieve from Vault path "mlops/s3"
        pass

    def get_model_signing_key(self) -> str:
        """Get private key for model signing."""
        # TODO: Retrieve from Vault path "mlops/signing-key"
        # TODO: Return private key
        pass

    def get_db_connection(self) -> Dict:
        """Get dynamic database connection credentials."""
        # TODO: Request dynamic credentials
        # TODO: Return connection info
        pass

    def refresh_all_credentials(self):
        """Refresh all short-lived credentials."""
        # TODO: Renew leases for dynamic credentials
        # TODO: Refresh cached credentials
        pass

# Example usage in training script

from src.security.secrets_manager import VaultSecretsManager, MLPipelineSecrets
import mlflow

def train_model_with_vault():
    """Train model with secrets from Vault."""
    # TODO: Initialize Vault
    vault = VaultSecretsManager(
        vault_url=os.getenv("VAULT_ADDR"),
        token=os.getenv("VAULT_TOKEN")
    )

    secrets = MLPipelineSecrets(vault)

    # TODO: Get MLflow credentials
    mlflow_creds = secrets.get_mlflow_credentials()

    # TODO: Configure MLflow
    mlflow.set_tracking_uri(mlflow_creds['tracking_uri'])
    os.environ['MLFLOW_TRACKING_USERNAME'] = mlflow_creds['username']
    os.environ['MLFLOW_TRACKING_PASSWORD'] = mlflow_creds['password']

    # TODO: Get database credentials
    db_creds = secrets.get_db_connection()

    # TODO: Train model with secure credentials
    # TODO: Log to MLflow

    # TODO: Clean up leases
    pass
```

### Vault Setup Script

```bash
# scripts/setup_vault.sh
#!/bin/bash
# Set up Vault for MLOps secrets management

# TODO: Start Vault dev server
vault server -dev &

# TODO: Export Vault address and token
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

# TODO: Enable KV v2 secrets engine
vault secrets enable -version=2 kv

# TODO: Store ML pipeline secrets
vault kv put secret/mlops/mlflow \
    tracking_uri='http://mlflow:5000' \
    username='mlflow_user' \
    password='secure_password_here'

vault kv put secret/mlops/s3 \
    aws_access_key_id='AKIA...' \
    aws_secret_access_key='secret...'

vault kv put secret/mlops/signing-key \
    private_key='-----BEGIN PRIVATE KEY-----...'

# TODO: Enable database secrets engine
vault secrets enable database

# TODO: Configure PostgreSQL connection
vault write database/config/training-db \
    plugin_name=postgresql-database-plugin \
    allowed_roles="ml-pipeline" \
    connection_url="postgresql://{{username}}:{{password}}@postgres:5432/mldb" \
    username="vault" \
    password="vault_password"

# TODO: Create role for dynamic credentials
vault write database/roles/ml-pipeline \
    db_name=training-db \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"

echo "Vault setup complete!"
```

### Docker Compose for Testing

```yaml
# docker-compose.vault.yml
version: '3.8'

services:
  vault:
    image: vault:latest
    ports:
      - "8200:8200"
    environment:
      VAULT_DEV_ROOT_TOKEN_ID: "root"
      VAULT_DEV_LISTEN_ADDRESS: "0.0.0.0:8200"
    cap_add:
      - IPC_LOCK

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: mldb
      POSTGRES_USER: vault
      POSTGRES_PASSWORD: vault_password
    ports:
      - "5432:5432"
```

### Validation Tests

```python
# tests/test_secrets_manager.py
import pytest
import hvac
from src.security.secrets_manager import VaultSecretsManager, MLPipelineSecrets

@pytest.fixture
def vault_manager():
    """Create Vault manager for testing."""
    # TODO: Connect to dev Vault
    manager = VaultSecretsManager(
        vault_url="http://localhost:8200",
        token="root"
    )
    yield manager
    # TODO: Cleanup after tests

def test_store_and_retrieve_secret(vault_manager):
    """Test storing and retrieving secret."""
    secret_data = {"password": "test123"}
    path = "test/secret1"

    # TODO: Store secret
    metadata = vault_manager.store_secret(path, secret_data)

    # TODO: Retrieve secret
    retrieved = vault_manager.get_secret(path)

    # TODO: Assert data matches
    assert retrieved['password'] == "test123"

def test_secret_rotation(vault_manager):
    """Test secret rotation creates new version."""
    path = "test/rotate-secret"

    # TODO: Store initial secret
    vault_manager.store_secret(path, {"key": "v1"})

    # TODO: Rotate secret
    vault_manager.rotate_secret(path, {"key": "v2"})

    # TODO: Get latest version
    latest = vault_manager.get_secret(path)
    assert latest['key'] == "v2"

    # TODO: Get version 1
    v1 = vault_manager.get_secret(path, version=1)
    assert v1['key'] == "v1"

def test_dynamic_database_credentials(vault_manager):
    """Test dynamic database credentials."""
    # TODO: Request dynamic credentials
    creds = vault_manager.create_db_credentials(
        db_name="training-db",
        role="ml-pipeline",
        ttl="5m"
    )

    # TODO: Assert credentials returned
    assert 'username' in creds
    assert 'password' in creds
    assert 'lease_id' in creds

    # TODO: Test credentials work (connect to database)

def test_ml_pipeline_secrets(vault_manager):
    """Test ML pipeline secrets integration."""
    # TODO: Setup test secrets
    # TODO: Create MLPipelineSecrets
    # TODO: Retrieve all credential types
    # TODO: Assert all work correctly
    pass
```

### Success Criteria

- [ ] Vault is running and accessible
- [ ] Secrets are stored and retrieved successfully
- [ ] Secret rotation creates new versions
- [ ] Dynamic database credentials are generated
- [ ] ML pipeline can retrieve all needed secrets
- [ ] Leases are renewed and revoked properly
- [ ] No secrets are hardcoded in code
- [ ] Credentials are not logged or printed

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Vault Client Initialization**:
```python
self.client = hvac.Client(url=vault_url, token=token or os.getenv('VAULT_TOKEN'))
if not self.client.is_authenticated():
    raise Exception("Vault authentication failed")
```

2. **Storing Secrets (KV v2)**:
```python
response = self.client.secrets.kv.v2.create_or_update_secret(
    path=path,
    secret=secret_data,
    mount_point=mount_point
)
return SecretMetadata(
    path=path,
    version=response['data']['version'],
    created_time=response['data']['created_time']
)
```

3. **Retrieving Secrets**:
```python
response = self.client.secrets.kv.v2.read_secret_version(
    path=path,
    version=version,
    mount_point=mount_point
)
return response['data']['data']
```

4. **Dynamic Database Credentials**:
```python
response = self.client.secrets.database.generate_credentials(
    name=role
)
return {
    'username': response['data']['username'],
    'password': response['data']['password'],
    'lease_id': response['lease_id']
}
```

5. **Best Practices**:
   - Use AppRole authentication in production (not tokens)
   - Enable audit logging
   - Use namespaces for multi-tenancy
   - Implement secrets rotation policies
   - Monitor lease renewals

</details>

---

## Exercise 3: Supply Chain Security (SLSA, SBOM, Cosign) (90 minutes)

**Objective**: Implement supply chain security for ML models and artifacts using SLSA, SBOM, and Cosign.

### Background

Ensure the integrity and provenance of ML models and dependencies throughout the supply chain. Implement Software Bill of Materials (SBOM), sign artifacts, and verify integrity.

### Tasks

1. **Generate SBOM for ML dependencies**
2. **Sign model artifacts with Cosign**
3. **Verify model signatures**
4. **Implement SLSA provenance**
5. **Create supply chain security policy**

### Starter Code

```python
# src/security/supply_chain.py
"""Supply chain security for ML models."""

import json
import subprocess
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import datetime

@dataclass
class Dependency:
    """Software dependency."""
    name: str
    version: str
    license: str
    source: str  # "pypi", "conda", "git"
    checksum: str

@dataclass
class SBOM:
    """Software Bill of Materials."""
    name: str
    version: str
    timestamp: str
    dependencies: List[Dependency]

    def to_json(self) -> str:
        """Convert to JSON."""
        # TODO: Convert to JSON format
        # TODO: Include SPDX or CycloneDX format
        pass

    def to_spdx(self) -> str:
        """Convert to SPDX format."""
        # TODO: Generate SPDX document
        pass

class SBOMGenerator:
    """Generate Software Bill of Materials."""

    def __init__(self, project_name: str, version: str):
        """
        Initialize SBOM generator.

        Args:
            project_name: Project name
            version: Project version
        """
        self.project_name = project_name
        self.version = version

    def generate_from_requirements(self, requirements_file: str) -> SBOM:
        """
        Generate SBOM from requirements.txt.

        Args:
            requirements_file: Path to requirements.txt

        Returns:
            SBOM object
        """
        # TODO: Parse requirements.txt
        # TODO: For each dependency:
        #   - Get version
        #   - Get license (from PyPI API)
        #   - Calculate checksum
        # TODO: Create SBOM
        pass

    def generate_from_environment(self) -> SBOM:
        """
        Generate SBOM from current Python environment.

        Returns:
            SBOM object
        """
        # TODO: Use pip freeze to get installed packages
        # TODO: Get metadata for each package
        # TODO: Create SBOM
        pass

    def add_model_artifact(
        self,
        sbom: SBOM,
        model_path: str,
        model_version: str
    ) -> SBOM:
        """
        Add model artifact to SBOM.

        Args:
            sbom: Existing SBOM
            model_path: Path to model file
            model_version: Model version

        Returns:
            Updated SBOM
        """
        # TODO: Calculate model checksum
        # TODO: Add as dependency
        # TODO: Return updated SBOM
        pass

    def scan_vulnerabilities(self, sbom: SBOM) -> List[Dict]:
        """
        Scan SBOM for known vulnerabilities.

        Args:
            sbom: SBOM to scan

        Returns:
            List of vulnerabilities found
        """
        # TODO: Use safety or similar tool
        # TODO: Check each dependency against vulnerability database
        # TODO: Return findings
        pass

class ModelSigner:
    """Sign and verify ML model artifacts."""

    def __init__(self, key_path: Optional[str] = None):
        """
        Initialize model signer.

        Args:
            key_path: Path to signing key (uses cosign key if None)
        """
        self.key_path = key_path

    def sign_model(
        self,
        model_path: str,
        output_signature: str = None
    ) -> str:
        """
        Sign model artifact using Cosign.

        Args:
            model_path: Path to model file
            output_signature: Where to save signature

        Returns:
            Path to signature file
        """
        # TODO: Calculate model hash
        # TODO: Sign using cosign
        # TODO: Command: cosign sign-blob --key <key> <model_path>
        # TODO: Save signature
        # TODO: Return signature path
        pass

    def verify_signature(
        self,
        model_path: str,
        signature_path: str,
        public_key_path: str
    ) -> bool:
        """
        Verify model signature.

        Args:
            model_path: Path to model file
            signature_path: Path to signature file
            public_key_path: Path to public key

        Returns:
            True if signature is valid, False otherwise
        """
        # TODO: Verify signature using cosign
        # TODO: Command: cosign verify-blob --key <public_key> --signature <sig> <model>
        # TODO: Return verification result
        pass

    def sign_container_image(
        self,
        image_ref: str,
        key_path: str = None
    ):
        """
        Sign container image.

        Args:
            image_ref: Container image reference (e.g., "myregistry/model:v1")
            key_path: Path to signing key
        """
        # TODO: Sign image with cosign
        # TODO: Command: cosign sign --key <key> <image>
        # TODO: Push signature to registry
        pass

    def verify_container_image(
        self,
        image_ref: str,
        public_key_path: str
    ) -> bool:
        """
        Verify container image signature.

        Args:
            image_ref: Container image reference
            public_key_path: Path to public key

        Returns:
            True if verified, False otherwise
        """
        # TODO: Verify image with cosign
        # TODO: Command: cosign verify --key <public_key> <image>
        pass

@dataclass
class SLSAProvenance:
    """SLSA provenance metadata."""
    builder: str
    build_type: str
    invocation: Dict
    metadata: Dict
    materials: List[Dict]  # Input artifacts

class ProvenanceGenerator:
    """Generate SLSA provenance."""

    def generate_provenance(
        self,
        model_path: str,
        training_script: str,
        data_sources: List[str],
        builder_id: str = "github-actions"
    ) -> SLSAProvenance:
        """
        Generate SLSA provenance for model.

        Args:
            model_path: Path to trained model
            training_script: Path to training script
            data_sources: List of data source URIs
            builder_id: Builder identifier

        Returns:
            SLSA provenance
        """
        # TODO: Collect build metadata
        # TODO: Hash all input materials (data, code)
        # TODO: Create provenance document
        # TODO: Sign provenance
        pass

    def verify_provenance(
        self,
        model_path: str,
        provenance: SLSAProvenance
    ) -> bool:
        """
        Verify model provenance.

        Args:
            model_path: Path to model
            provenance: SLSA provenance

        Returns:
            True if provenance is valid
        """
        # TODO: Verify model hash matches provenance
        # TODO: Verify builder signature
        # TODO: Check materials haven't changed
        pass

# Example usage

def secure_model_pipeline():
    """Example secure ML pipeline with supply chain security."""
    # TODO: Generate SBOM
    sbom_gen = SBOMGenerator("fraud-detection", "1.0.0")
    sbom = sbom_gen.generate_from_requirements("requirements.txt")

    # TODO: Add model to SBOM
    sbom = sbom_gen.add_model_artifact(sbom, "model.pkl", "1.0.0")

    # TODO: Scan for vulnerabilities
    vulns = sbom_gen.scan_vulnerabilities(sbom)
    if vulns:
        print(f"WARNING: {len(vulns)} vulnerabilities found!")

    # TODO: Save SBOM
    with open("sbom.json", "w") as f:
        f.write(sbom.to_json())

    # TODO: Sign model
    signer = ModelSigner()
    signature = signer.sign_model("model.pkl", "model.pkl.sig")

    # TODO: Generate provenance
    prov_gen = ProvenanceGenerator()
    provenance = prov_gen.generate_provenance(
        model_path="model.pkl",
        training_script="train.py",
        data_sources=["s3://data/training.csv"],
        builder_id="github-actions-runner-1"
    )

    # TODO: Save provenance
    with open("provenance.json", "w") as f:
        json.dump(asdict(provenance), f, indent=2)

    print("✓ Model secured with SBOM, signature, and provenance")
```

### GitHub Actions Workflow

```yaml
# .github/workflows/secure-build.yml
name: Secure ML Model Build

on:
  push:
    branches: [main]

jobs:
  build-and-sign:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write  # For keyless signing

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install cyclonedx-bom cosign

      # TODO: Generate SBOM
      - name: Generate SBOM
        run: |
          cyclonedx-py -r -i requirements.txt -o sbom.json

      # TODO: Train model
      - name: Train model
        run: python train.py

      # TODO: Install Cosign
      - name: Install Cosign
        uses: sigstore/cosign-installer@v3

      # TODO: Sign model (keyless with GitHub OIDC)
      - name: Sign model artifact
        run: |
          cosign sign-blob --yes model.pkl > model.pkl.sig

      # TODO: Generate provenance
      - name: Generate SLSA provenance
        run: |
          python scripts/generate_provenance.py \
            --model model.pkl \
            --script train.py \
            --output provenance.json

      # TODO: Upload artifacts
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: secured-model
          path: |
            model.pkl
            model.pkl.sig
            sbom.json
            provenance.json
```

### Validation Tests

```python
# tests/test_supply_chain.py
import pytest
from src.security.supply_chain import (
    SBOMGenerator, ModelSigner, ProvenanceGenerator
)

def test_sbom_generation():
    """Test SBOM generation from requirements."""
    # TODO: Create test requirements.txt
    # TODO: Generate SBOM
    # TODO: Assert contains expected dependencies
    pass

def test_model_signing_and_verification(tmp_path):
    """Test model signing and signature verification."""
    # TODO: Create test model file
    # TODO: Generate cosign key pair
    # TODO: Sign model
    # TODO: Verify signature
    # TODO: Assert verification succeeds

    # TODO: Modify model
    # TODO: Assert verification fails
    pass

def test_sbom_vulnerability_scan():
    """Test vulnerability scanning."""
    # TODO: Create SBOM with known vulnerable package
    # TODO: Run vulnerability scan
    # TODO: Assert vulnerabilities found
    pass

def test_provenance_generation():
    """Test SLSA provenance generation."""
    # TODO: Create test model and materials
    # TODO: Generate provenance
    # TODO: Assert provenance contains expected metadata
    # TODO: Verify provenance
    pass
```

### Success Criteria

- [ ] SBOM is generated with all dependencies
- [ ] SBOM includes licenses and checksums
- [ ] Model artifacts are signed with Cosign
- [ ] Signatures can be verified successfully
- [ ] Modified artifacts fail verification
- [ ] Vulnerability scanning detects known issues
- [ ] SLSA provenance is generated
- [ ] Container images are signed and verified
- [ ] GitHub Actions workflow runs successfully

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Generate SBOM with CycloneDX**:
```bash
pip install cyclonedx-bom
cyclonedx-py -r -i requirements.txt -o sbom.json
```

2. **Sign with Cosign**:
```bash
# Generate key pair
cosign generate-key-pair

# Sign blob
cosign sign-blob --key cosign.key model.pkl > model.pkl.sig

# Verify blob
cosign verify-blob --key cosign.pub --signature model.pkl.sig model.pkl
```

3. **Sign Container Image**:
```bash
cosign sign --key cosign.key myregistry/model:v1
cosign verify --key cosign.pub myregistry/model:v1
```

4. **Calculate File Hash**:
```python
def calculate_hash(filepath: str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()
```

5. **Vulnerability Scanning**: Use `safety check` or integrate with Snyk/Grype

</details>

---

## Exercise 4: Container & Runtime Security (90 minutes)

**Objective**: Implement container security scanning and runtime security for ML deployments.

### Background

Secure ML containers using vulnerability scanning, policy enforcement, and runtime protection. Implement defense-in-depth for containerized ML workloads.

### Tasks

1. **Scan container images for vulnerabilities**
2. **Implement least-privilege container configs**
3. **Create security policies with OPA**
4. **Implement runtime security monitoring**
5. **Harden container deployment**

### Starter Code

```python
# src/security/container_security.py
"""Container and runtime security."""

import subprocess
import json
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Vulnerability:
    """Container vulnerability."""
    cve_id: str
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    package: str
    installed_version: str
    fixed_version: str
    description: str

class ContainerScanner:
    """Scan containers for vulnerabilities."""

    def __init__(self, scanner: str = "trivy"):
        """
        Initialize container scanner.

        Args:
            scanner: Scanner to use ("trivy", "grype", "snyk")
        """
        self.scanner = scanner

    def scan_image(
        self,
        image_ref: str,
        severity_threshold: str = "HIGH"
    ) -> List[Vulnerability]:
        """
        Scan container image for vulnerabilities.

        Args:
            image_ref: Container image reference
            severity_threshold: Minimum severity to report

        Returns:
            List of vulnerabilities found
        """
        # TODO: Run scanner (e.g., trivy image <image_ref>)
        # TODO: Parse JSON output
        # TODO: Filter by severity threshold
        # TODO: Create Vulnerability objects
        # TODO: Return list
        pass

    def scan_dockerfile(self, dockerfile_path: str) -> List[str]:
        """
        Scan Dockerfile for security issues.

        Args:
            dockerfile_path: Path to Dockerfile

        Returns:
            List of security recommendations
        """
        # TODO: Check for:
        #   - Running as root
        #   - Using latest tag
        #   - Secrets in build
        #   - Unnecessary packages
        # TODO: Return recommendations
        pass

    def generate_report(
        self,
        vulnerabilities: List[Vulnerability],
        output_path: str = "security-report.html"
    ):
        """Generate security report."""
        # TODO: Create HTML report with vulnerability details
        # TODO: Include remediation steps
        # TODO: Add summary statistics
        pass

class ContainerHardening:
    """Container hardening configurations."""

    @staticmethod
    def create_secure_dockerfile() -> str:
        """
        Create hardened Dockerfile for ML serving.

        Returns:
            Dockerfile contents
        """
        # TODO: Return hardened Dockerfile with:
        #   - Specific base image version (not latest)
        #   - Non-root user
        #   - Minimal dependencies
        #   - No secrets
        #   - Health checks
        #   - Read-only filesystem where possible
        return """
# TODO: Implement secure Dockerfile
FROM python:3.9-slim AS base

# Create non-root user
RUN useradd -m -u 1000 mluser

# Install dependencies as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# TODO: Add more hardening steps
"""

    @staticmethod
    def create_k8s_security_context() -> Dict:
        """
        Create Kubernetes security context.

        Returns:
            Security context configuration
        """
        # TODO: Return security context with:
        #   - runAsNonRoot
        #   - readOnlyRootFilesystem
        #   - allowPrivilegeEscalation: false
        #   - capabilities drop
        return {
            "securityContext": {
                # TODO: Implement
                "runAsNonRoot": True,
                "runAsUser": 1000,
                "readOnlyRootFilesystem": True,
                "allowPrivilegeEscalation": False,
                "capabilities": {
                    "drop": ["ALL"]
                }
            },
            "resources": {
                "limits": {
                    "cpu": "1000m",
                    "memory": "1Gi"
                },
                "requests": {
                    "cpu": "500m",
                    "memory": "512Mi"
                }
            }
        }

    @staticmethod
    def create_pod_security_policy() -> Dict:
        """
        Create Pod Security Policy.

        Returns:
            PSP configuration
        """
        # TODO: Define restrictive PSP
        pass

class OPAPolicyEngine:
    """Open Policy Agent policy enforcement."""

    def __init__(self):
        """Initialize OPA engine."""
        pass

    def create_admission_policy(self) -> str:
        """
        Create OPA admission policy for ML workloads.

        Returns:
            Rego policy
        """
        # TODO: Create Rego policy that enforces:
        #   - All containers must run as non-root
        #   - Resource limits must be set
        #   - Images must be from approved registries
        #   - Images must be signed
        return """
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.securityContext.runAsNonRoot
    msg := sprintf("Container %v must run as non-root", [container.name])
}

# TODO: Add more policies
"""

    def validate_deployment(self, deployment_yaml: str) -> List[str]:
        """
        Validate deployment against policies.

        Args:
            deployment_yaml: Kubernetes deployment YAML

        Returns:
            List of policy violations
        """
        # TODO: Run OPA evaluation
        # TODO: Return violations
        pass

class RuntimeSecurity:
    """Runtime security monitoring."""

    def __init__(self):
        """Initialize runtime security."""
        pass

    def monitor_syscalls(self, container_id: str) -> List[Dict]:
        """
        Monitor syscalls in container (using Falco rules).

        Args:
            container_id: Container ID to monitor

        Returns:
            List of suspicious events
        """
        # TODO: Integrate with Falco
        # TODO: Monitor for:
        #   - Unexpected network connections
        #   - File modifications
        #   - Privilege escalation attempts
        # TODO: Return suspicious events
        pass

    def detect_anomalies(
        self,
        container_metrics: Dict
    ) -> List[str]:
        """
        Detect runtime anomalies.

        Args:
            container_metrics: Container resource usage

        Returns:
            List of detected anomalies
        """
        # TODO: Analyze metrics for anomalies:
        #   - Unexpected CPU spikes
        #   - High network traffic
        #   - Memory leaks
        # TODO: Return anomalies
        pass

# Example secure deployment

def deploy_secure_ml_service():
    """Deploy ML service with security controls."""
    # TODO: Scan image
    scanner = ContainerScanner()
    vulns = scanner.scan_image("myregistry/ml-model:v1")

    critical_vulns = [v for v in vulns if v.severity == "CRITICAL"]
    if critical_vulns:
        raise Exception(f"Cannot deploy: {len(critical_vulns)} critical vulnerabilities")

    # TODO: Generate secure Kubernetes manifest
    hardening = ContainerHardening()
    security_context = hardening.create_k8s_security_context()

    # TODO: Validate with OPA
    opa = OPAPolicyEngine()
    violations = opa.validate_deployment("deployment.yaml")
    if violations:
        raise Exception(f"Policy violations: {violations}")

    # TODO: Deploy
    print("✓ Security checks passed, deploying...")
```

### Dockerfile Examples

```dockerfile
# Dockerfile.insecure (DON'T USE)
FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "serve.py"]

# TODO: Identify security issues:
# - Using 'latest' tag
# - Running as root
# - No user specified
# - No resource limits
# - Secrets might be copied
```

```dockerfile
# Dockerfile.secure (USE THIS)
# Multi-stage build for smaller image
FROM python:3.9-slim AS builder

WORKDIR /build

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.9-slim

# Create non-root user
RUN useradd -m -u 1000 mluser && \
    mkdir /app && \
    chown mluser:mluser /app

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder --chown=mluser:mluser /root/.local /home/mluser/.local

# Copy application
COPY --chown=mluser:mluser serve.py .
COPY --chown=mluser:mluser model/ model/

# Switch to non-root user
USER mluser

# Set PATH
ENV PATH=/home/mluser/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Expose port
EXPOSE 8000

# Run
CMD ["python", "serve.py"]
```

### Kubernetes Deployment

```yaml
# k8s/deployment-secure.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-serving
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-model
  template:
    metadata:
      labels:
        app: ml-model
    spec:
      # TODO: Security settings
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      containers:
      - name: model-server
        image: myregistry/ml-model:v1.0.0  # Specific version, not latest

        # Container security context
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
              - ALL

        # Resource limits
        resources:
          limits:
            cpu: "1000m"
            memory: "1Gi"
          requests:
            cpu: "500m"
            memory: "512Mi"

        # Health checks
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10

        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

        # Volume mounts (read-only)
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: model-cache
          mountPath: /app/.cache

      volumes:
      - name: tmp
        emptyDir: {}
      - name: model-cache
        emptyDir: {}
```

### Validation Tests

```python
# tests/test_container_security.py
import pytest
from src.security.container_security import (
    ContainerScanner, ContainerHardening, OPAPolicyEngine
)

def test_vulnerability_scanning():
    """Test container vulnerability scanning."""
    scanner = ContainerScanner("trivy")

    # TODO: Scan test image
    vulns = scanner.scan_image("python:3.9-slim")

    # TODO: Assert scan completed
    # TODO: Check vulnerability structure
    pass

def test_dockerfile_security_check():
    """Test Dockerfile security analysis."""
    # TODO: Create insecure Dockerfile
    # TODO: Scan for issues
    # TODO: Assert issues are detected
    pass

def test_opa_policy_enforcement():
    """Test OPA policy validation."""
    opa = OPAPolicyEngine()

    # TODO: Create deployment with security violations
    # TODO: Validate against policy
    # TODO: Assert violations detected
    pass

def test_secure_k8s_manifest_generation():
    """Test secure Kubernetes manifest creation."""
    hardening = ContainerHardening()

    security_context = hardening.create_k8s_security_context()

    # TODO: Assert non-root
    assert security_context['securityContext']['runAsNonRoot'] == True

    # TODO: Assert read-only filesystem
    # TODO: Assert capabilities dropped
    pass
```

### Success Criteria

- [ ] Container images are scanned for vulnerabilities
- [ ] Critical vulnerabilities block deployment
- [ ] Containers run as non-root user
- [ ] Resource limits are enforced
- [ ] Read-only root filesystem where possible
- [ ] OPA policies enforce security requirements
- [ ] Runtime monitoring detects suspicious activity
- [ ] Security context is properly configured
- [ ] Images use specific tags, not 'latest'

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Scan with Trivy**:
```bash
trivy image --severity HIGH,CRITICAL python:3.9-slim
trivy image --format json --output results.json myimage:v1
```

2. **Scan with Grype**:
```bash
grype myregistry/ml-model:v1
```

3. **OPA Policy Example**:
```rego
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources.limits.memory
    msg := sprintf("Container %v must have memory limit", [container.name])
}
```

4. **Test OPA Policy**:
```bash
opa eval -d policy.rego -i input.json "data.kubernetes.admission.deny"
```

5. **Falco Rules** for runtime monitoring

</details>

---

## Exercise 5: Complete MLOps Security Framework (120 minutes)

**Objective**: Integrate all security components into a comprehensive MLOps security framework.

### Background

Build an end-to-end secure MLOps pipeline incorporating threat modeling, secrets management, supply chain security, and runtime protection.

### Tasks

1. **Design comprehensive security architecture**
2. **Implement secure CI/CD pipeline**
3. **Deploy with all security controls**
4. **Create security monitoring dashboard**
5. **Document security procedures**

### Starter Code

```python
# src/security/framework.py
"""Complete MLOps security framework."""

from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

from src.security.threat_model import ThreatModel
from src.security.secrets_manager import VaultSecretsManager
from src.security.supply_chain import SBOMGenerator, ModelSigner
from src.security.container_security import ContainerScanner, ContainerHardening

@dataclass
class SecurityConfig:
    """Security configuration."""
    vault_url: str
    vault_token: str
    enable_model_signing: bool = True
    enable_sbom: bool = True
    enable_container_scanning: bool = True
    vulnerability_threshold: str = "HIGH"
    signing_key_path: Optional[str] = None

class MLOpsSecurityFramework:
    """Comprehensive MLOps security framework."""

    def __init__(self, config: SecurityConfig):
        """
        Initialize security framework.

        Args:
            config: Security configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

        # TODO: Initialize components
        self.vault = VaultSecretsManager(config.vault_url, config.vault_token)
        self.sbom_gen = None
        self.signer = None
        self.scanner = None

        self._initialize_components()

    def _initialize_components(self):
        """Initialize security components."""
        # TODO: Initialize SBOM generator
        # TODO: Initialize model signer
        # TODO: Initialize container scanner
        pass

    def secure_training_pipeline(
        self,
        model_name: str,
        version: str,
        training_script: str,
        data_sources: List[str]
    ) -> Dict:
        """
        Execute secure training pipeline.

        Args:
            model_name: Model name
            version: Model version
            training_script: Path to training script
            data_sources: List of data source URIs

        Returns:
            Security artifacts
        """
        self.logger.info(f"Starting secure training for {model_name}:{version}")

        artifacts = {}

        # TODO: 1. Get secrets from Vault
        db_creds = self.vault.get_secret("mlops/database")

        # TODO: 2. Generate SBOM
        if self.config.enable_sbom:
            sbom = self.sbom_gen.generate_from_environment()
            artifacts['sbom'] = sbom

        # TODO: 3. Train model (with secrets)
        # model = train_model(db_creds)

        # TODO: 4. Sign model
        if self.config.enable_model_signing:
            signature = self.signer.sign_model(f"{model_name}.pkl")
            artifacts['signature'] = signature

        # TODO: 5. Generate provenance
        # provenance = generate_provenance(...)
        # artifacts['provenance'] = provenance

        # TODO: 6. Scan for vulnerabilities
        vulns = self.sbom_gen.scan_vulnerabilities(sbom)
        artifacts['vulnerabilities'] = vulns

        if any(v['severity'] == 'CRITICAL' for v in vulns):
            raise Exception("Critical vulnerabilities found, blocking deployment")

        return artifacts

    def secure_deployment_pipeline(
        self,
        image_ref: str,
        deployment_manifest: str
    ) -> bool:
        """
        Execute secure deployment pipeline.

        Args:
            image_ref: Container image reference
            deployment_manifest: Path to K8s manifest

        Returns:
            True if deployment approved, False otherwise
        """
        self.logger.info(f"Validating deployment: {image_ref}")

        # TODO: 1. Scan container image
        if self.config.enable_container_scanning:
            vulns = self.scanner.scan_image(
                image_ref,
                severity_threshold=self.config.vulnerability_threshold
            )

            if vulns:
                self.logger.error(f"Found {len(vulns)} vulnerabilities")
                return False

        # TODO: 2. Verify image signature
        # is_verified = self.signer.verify_container_image(image_ref, public_key)
        # if not is_verified:
        #     return False

        # TODO: 3. Validate deployment manifest
        # violations = validate_manifest(deployment_manifest)
        # if violations:
        #     return False

        # TODO: 4. Deploy with security context
        # apply_secure_deployment(deployment_manifest)

        self.logger.info("✓ Deployment security checks passed")
        return True

    def generate_security_report(self, output_path: str = "security-report.md"):
        """
        Generate comprehensive security report.

        Args:
            output_path: Path to save report
        """
        # TODO: Aggregate security metrics:
        #   - Threat model summary
        #   - Vulnerability scan results
        #   - Secret rotation status
        #   - Compliance status
        # TODO: Generate markdown report
        # TODO: Save to file
        pass

    def audit_security_controls(self) -> Dict:
        """
        Audit all security controls.

        Returns:
            Audit results
        """
        audit_results = {
            'secrets_management': False,
            'model_signing': False,
            'container_scanning': False,
            'runtime_protection': False,
            'compliance': {}
        }

        # TODO: Check Vault connectivity
        # TODO: Verify signing keys present
        # TODO: Test scanner
        # TODO: Check runtime monitoring
        # TODO: Return audit results

        return audit_results

# Secure CI/CD Pipeline

def secure_ci_cd_pipeline(
    model_name: str,
    version: str,
    git_repo: str,
    git_commit: str
):
    """
    Secure CI/CD pipeline for ML models.

    Args:
        model_name: Model name
        version: Model version
        git_repo: Git repository URL
        git_commit: Git commit SHA
    """
    # TODO: Initialize security framework
    config = SecurityConfig(
        vault_url="http://vault:8200",
        vault_token=os.getenv("VAULT_TOKEN"),
        enable_model_signing=True,
        enable_sbom=True,
        enable_container_scanning=True
    )

    framework = MLOpsSecurityFramework(config)

    # TODO: 1. Checkout code
    # checkout(git_repo, git_commit)

    # TODO: 2. Run security scans on code
    # run_sast_scan()
    # run_dependency_scan()

    # TODO: 3. Secure training
    artifacts = framework.secure_training_pipeline(
        model_name=model_name,
        version=version,
        training_script="train.py",
        data_sources=["s3://data/train.csv"]
    )

    # TODO: 4. Build container
    image_ref = f"myregistry/{model_name}:{version}"
    # build_container(image_ref)

    # TODO: 5. Scan container
    # TODO: 6. Sign container
    # TODO: 7. Push to registry

    # TODO: 8. Deploy
    approved = framework.secure_deployment_pipeline(
        image_ref=image_ref,
        deployment_manifest="k8s/deployment.yaml"
    )

    if not approved:
        raise Exception("Deployment blocked by security controls")

    # TODO: 9. Generate security report
    framework.generate_security_report()

    print("✓ Secure CI/CD pipeline completed successfully")
```

### Complete GitHub Actions Workflow

```yaml
# .github/workflows/secure-mlops-pipeline.yml
name: Secure MLOps Pipeline

on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # TODO: SAST scanning
      - name: Run SAST with Semgrep
        run: |
          pip install semgrep
          semgrep --config=auto --json --output=sast-results.json

      # TODO: Dependency scanning
      - name: Scan dependencies
        run: |
          pip install safety
          safety check --json > dependency-scan.json

      # TODO: Secret scanning
      - name: Scan for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

  threat-model:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Generate threat model
        run: |
          python scripts/create_threat_model.py

      - name: Upload threat model
        uses: actions/upload-artifact@v3
        with:
          name: threat-model
          path: threat_model.json

  build-and-sign:
    needs: [security-scan, threat-model]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      id-token: write

    steps:
      - uses: actions/checkout@v3

      # TODO: Get secrets from Vault
      - name: Get secrets from Vault
        uses: hashicorp/vault-action@v2
        with:
          url: ${{ secrets.VAULT_ADDR }}
          method: jwt
          role: github-actions
          secrets: |
            secret/data/mlops/mlflow username | MLFLOW_USERNAME ;
            secret/data/mlops/mlflow password | MLFLOW_PASSWORD

      # TODO: Generate SBOM
      - name: Generate SBOM
        run: |
          pip install cyclonedx-bom
          cyclonedx-py -r -i requirements.txt -o sbom.json

      # TODO: Train model
      - name: Train model
        run: python train.py
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_URI }}
          MLFLOW_TRACKING_USERNAME: ${{ env.MLFLOW_USERNAME }}
          MLFLOW_TRACKING_PASSWORD: ${{ env.MLFLOW_PASSWORD }}

      # TODO: Sign model
      - name: Install Cosign
        uses: sigstore/cosign-installer@v3

      - name: Sign model artifact
        run: cosign sign-blob --yes model.pkl > model.pkl.sig

      # TODO: Build container
      - name: Build Docker image
        run: docker build -t ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} -f Dockerfile.secure .

      # TODO: Scan container
      - name: Scan container with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          exit-code: '1'
          severity: 'CRITICAL,HIGH'

      # TODO: Sign container
      - name: Sign container image
        run: |
          cosign sign --yes ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

      # TODO: Push to registry
      - name: Push image
        run: docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

      # TODO: Generate security report
      - name: Generate security report
        run: python scripts/generate_security_report.py

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: security-artifacts
          path: |
            sbom.json
            model.pkl.sig
            security-report.md

  deploy:
    needs: build-and-sign
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # TODO: Verify image signature
      - name: Verify image signature
        run: |
          cosign verify ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

      # TODO: Deploy to Kubernetes
      - name: Deploy to K8s
        run: |
          kubectl apply -f k8s/deployment-secure.yaml
```

### Security Monitoring Dashboard

```python
# src/security/monitoring.py
"""Security monitoring dashboard."""

import prometheus_client as prom
from typing import Dict

# Metrics
security_scan_duration = prom.Histogram(
    'security_scan_duration_seconds',
    'Time spent scanning',
    ['scan_type']
)

vulnerabilities_found = prom.Gauge(
    'vulnerabilities_found_total',
    'Number of vulnerabilities found',
    ['severity', 'component']
)

model_signatures_verified = prom.Counter(
    'model_signatures_verified_total',
    'Number of model signatures verified',
    ['status']
)

secret_rotations = prom.Counter(
    'secret_rotations_total',
    'Number of secret rotations',
    ['secret_type']
)

def record_security_metrics(scan_results: Dict):
    """Record security metrics for monitoring."""
    # TODO: Record vulnerability counts
    # TODO: Record scan durations
    # TODO: Record signature verifications
    # TODO: Expose metrics endpoint
    pass
```

### Success Criteria

- [ ] Complete security framework integrates all components
- [ ] Secrets are managed through Vault
- [ ] All artifacts are signed and verified
- [ ] Container images are scanned before deployment
- [ ] Deployment blocked for critical vulnerabilities
- [ ] Security monitoring dashboard shows metrics
- [ ] CI/CD pipeline includes all security gates
- [ ] Security report is generated automatically
- [ ] Audit confirms all controls are functional
- [ ] Documentation is comprehensive

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Integration Pattern**: Chain security checks in pipeline:
```python
vault → sbom → train → sign → scan → verify → deploy
```

2. **Security Gates**: Block on:
   - Critical vulnerabilities
   - Failed signature verification
   - Policy violations
   - Missing security controls

3. **Monitoring**: Track security metrics:
   - Vulnerability counts by severity
   - Scan success/failure rates
   - Signature verification results
   - Secret rotation frequency

4. **Automation**: Use GitHub Actions or similar CI/CD to automate all security checks

5. **Documentation**: Include runbooks for:
   - Security incident response
   - Secret rotation procedures
   - Vulnerability remediation
   - Audit procedures

</details>

---

## Bonus Challenges

### Challenge 1: Implement Federated Learning Security

Implement secure federated learning with encrypted model updates and differential privacy.

### Challenge 2: Model Watermarking

Implement model watermarking to prove ownership and detect unauthorized use.

### Challenge 3: Zero-Trust ML Architecture

Design and implement a zero-trust architecture for ML systems.

---

## Additional Resources

- **OWASP ML Top 10**: [https://owasp.org/www-project-machine-learning-security-top-10/](https://owasp.org/www-project-machine-learning-security-top-10/)
- **HashiCorp Vault**: [https://www.vaultproject.io/docs](https://www.vaultproject.io/docs)
- **Sigstore/Cosign**: [https://docs.sigstore.dev/](https://docs.sigstore.dev/)
- **SLSA Framework**: [https://slsa.dev/](https://slsa.dev/)
- **Trivy Scanner**: [https://aquasecurity.github.io/trivy/](https://aquasecurity.github.io/trivy/)
- **OPA**: [https://www.openpolicyagent.org/](https://www.openpolicyagent.org/)

---

## Submission Guidelines

For each exercise, submit:
1. **Code**: All implementation files with security controls
2. **Tests**: Passing security validation tests
3. **Configurations**: Security policies, Dockerfiles, K8s manifests
4. **Documentation**: Threat model, security report, runbooks
5. **Evidence**: Scan results, signatures, SBOMs

**Estimated Total Time**: 6-9 hours
**Difficulty**: Advanced

Good luck securing your MLOps pipelines!
