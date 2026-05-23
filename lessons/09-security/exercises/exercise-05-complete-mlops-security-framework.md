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
