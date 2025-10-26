# Contributing to AI Infrastructure MLOps Learning

Thank you for your interest in contributing to the AI Infrastructure MLOps Engineer curriculum! This repository is designed to help aspiring MLOps engineers learn production-grade machine learning operations.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Contributing Content](#contributing-content)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project adheres to a Code of Conduct (see CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

**Before submitting a bug report:**
- Check the existing issues to avoid duplicates
- Verify the bug exists in the latest version
- Collect information about your environment

**When submitting a bug report, include:**
- Clear, descriptive title
- Exact steps to reproduce
- Expected vs actual behavior
- Code samples or error messages
- Your environment (OS, Python version, dependency versions)

### Suggesting Enhancements

We welcome suggestions for:
- New exercises or projects
- Additional topics or modules
- Tool or framework updates
- Improved explanations
- Additional resources

**Enhancement suggestions should include:**
- Clear description of the proposed feature
- Rationale and use cases
- Examples or mockups if applicable
- Any implementation considerations

### Contributing Content

We especially welcome contributions that:

1. **Update outdated content**: MLOps tools evolve rapidly
2. **Add real-world examples**: Share your production experiences
3. **Improve explanations**: Make complex topics more accessible
4. **Fix errors**: Correct technical inaccuracies or typos
5. **Expand exercises**: Add variations or advanced challenges
6. **Create new resources**: Links to articles, videos, or tools

## Pull Request Process

1. **Fork the repository** and create a branch from `main`
2. **Make your changes** following the style guidelines
3. **Test your changes**:
   - For code: Ensure all stubs run without errors
   - For exercises: Verify instructions are clear and complete
   - For documentation: Check for broken links and formatting
4. **Update documentation** if you're changing functionality
5. **Commit with clear messages** describing what and why
6. **Submit a pull request** with:
   - Description of changes
   - Related issue number (if applicable)
   - Testing performed
   - Screenshots (if UI/visual changes)

### PR Title Format

Use conventional commit format:
- `feat: Add exercise on model monitoring with Evidently`
- `fix: Correct MLflow tracking URI in Module 01`
- `docs: Update Kubernetes deployment instructions`
- `chore: Update dependencies to latest versions`

## Style Guidelines

### General Writing

- **Clarity**: Use clear, concise language
- **Consistency**: Follow existing patterns and terminology
- **Accuracy**: Verify technical details
- **Accessibility**: Explain jargon and acronyms
- **Examples**: Provide concrete examples where possible

### Code Style

- **Python**: Follow PEP 8 style guide
- **Formatting**: Use Black formatter (line length 88)
- **Type hints**: Include type hints for function signatures
- **Docstrings**: Use Google-style docstrings
- **Comments**: Explain "why" not "what"

Example:
```python
from typing import Dict, List
import mlflow


def log_model_metrics(metrics: Dict[str, float], run_id: str) -> None:
    """Log model evaluation metrics to MLflow.

    Args:
        metrics: Dictionary of metric names to values
        run_id: MLflow run identifier

    Raises:
        ValueError: If metrics dictionary is empty
    """
    if not metrics:
        raise ValueError("Metrics dictionary cannot be empty")

    with mlflow.start_run(run_id=run_id):
        mlflow.log_metrics(metrics)
```

### YAML Style

- **Indentation**: 2 spaces
- **Comments**: Explain configuration choices
- **Naming**: Use kebab-case for keys

### Markdown Style

- **Headers**: Use ATX-style headers (`#`, `##`, `###`)
- **Lists**: Use `-` for unordered, `1.` for ordered
- **Code blocks**: Always specify language for syntax highlighting
- **Links**: Use reference-style for repeated links
- **Line length**: Wrap at 120 characters for readability

### Exercise Guidelines

When creating or updating exercises:

1. **Clear objectives**: State what students will learn
2. **Prerequisites**: List required knowledge/completed modules
3. **Time estimate**: Provide realistic completion time
4. **Step-by-step**: Break complex tasks into steps
5. **Hints**: Include hints for common stumbling blocks
6. **Validation**: Explain how to verify correct completion
7. **Bonus challenges**: Add optional extensions

Example exercise structure:
```markdown
# Exercise 03: Implement Data Drift Detection

**Duration**: 90 minutes
**Prerequisites**: Module 03, basic Python, pandas

## Objective
Implement data drift detection using Kolmogorov-Smirnov test to identify when model retraining is needed.

## Steps

### Step 1: Set up the environment (10 min)
Install required dependencies:
\`\`\`bash
pip install evidently pandas scikit-learn
\`\`\`

### Step 2: Load reference and current data (15 min)
...

## Validation
Your implementation should:
- Detect drift on the synthetic drift dataset (drift_score > 0.3)
- Not detect drift on the stable dataset (drift_score < 0.1)

## Bonus Challenge
- Add multiple drift detection methods (PSI, Chi-square)
- Create automated alerts when drift exceeds threshold
```

### Documentation Guidelines

- **Completeness**: Cover all necessary information
- **Organization**: Use logical structure and navigation
- **Updates**: Keep documentation synchronized with code
- **Links**: Provide links to official documentation
- **Versioning**: Note version-specific information

## Development Setup

To set up your development environment:

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/ai-infra-mlops-learning.git
cd ai-infra-mlops-learning

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## Testing

Before submitting:

```bash
# Run code validation
python scripts/validate_stubs.py

# Check formatting
black --check lessons/

# Run linter
flake8 lessons/

# Check type hints
mypy lessons/
```

## Questions?

- **General questions**: Open a discussion in GitHub Discussions
- **Specific bugs**: Create an issue with the bug report template
- **Feature ideas**: Create an issue with the feature request template
- **Quick questions**: Join our community Discord (link in README)

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special recognition for major content additions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make MLOps education better for everyone!**
