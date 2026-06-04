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
