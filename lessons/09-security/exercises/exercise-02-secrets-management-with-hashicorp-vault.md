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
