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
