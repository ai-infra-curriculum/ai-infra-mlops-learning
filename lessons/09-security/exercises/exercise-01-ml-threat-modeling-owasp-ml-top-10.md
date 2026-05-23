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
