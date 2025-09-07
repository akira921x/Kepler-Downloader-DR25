# Contributing to Kepler-Downloader-DR25

Thank you for your interest in contributing to Kepler-Downloader-DR25! This document provides guidelines and instructions for contributing to this project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a branch** for your changes
4. **Make your changes** following our guidelines
5. **Test your changes** thoroughly
6. **Submit a pull request**

## How to Contribute

### Ways to Contribute

- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new features or improvements
- **Documentation**: Improve or translate documentation
- **Code**: Submit bug fixes or new features
- **Testing**: Add tests or improve test coverage
- **Performance**: Optimize code for better performance

### First-Time Contributors

Look for issues labeled with:
- `good first issue` - Simple tasks suitable for beginners
- `help wanted` - Issues where we need community help
- `documentation` - Documentation improvements

## Development Setup

### Prerequisites

```bash
# Python 3.7+
python --version

# Redis server
redis-cli ping

# Git
git --version
```

### Setup Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Kepler-Downloader-DR25.git
cd Kepler-Downloader-DR25

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Project Structure

```
Kepler-Downloader-DR25/
├── kepler_downloader_dr25/    # Main package code
│   ├── __init__.py
│   ├── downloader.py          # Main downloader module
│   ├── filter.py              # Filter module
│   └── utils/                 # Utility modules
├── tests/                     # Test files
│   ├── test_downloader.py
│   ├── test_filter.py
│   └── fixtures/              # Test data
├── docs/                      # Documentation
├── input_samples/             # Sample input files
└── requirements.txt           # Dependencies
```

## Code Standards

### Python Style Guide

We follow PEP 8 with these key points:

```python
# Good: Descriptive variable names
kepler_object_id = "006922244"
download_status = True

# Bad: Single letter variables (except in loops)
k = "006922244"
s = True

# Good: Clear function names
def download_kepler_data(kic_id, output_dir):
    """Download Kepler data for a specific KIC ID."""
    pass

# Good: Type hints (Python 3.7+)
from typing import List, Optional

def process_kics(kic_list: List[str], workers: int = 4) -> Optional[dict]:
    """Process a list of KIC IDs."""
    pass
```

### Code Quality Tools

```bash
# Format code with black
black kepler_downloader_dr25/ tests/

# Check style with flake8
flake8 kepler_downloader_dr25/ tests/

# Sort imports with isort
isort kepler_downloader_dr25/ tests/

# Type checking with mypy
mypy kepler_downloader_dr25/
```

### Commit Messages

Follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Examples:**
```bash
# Good commit messages
git commit -m "feat(downloader): add retry mechanism for failed downloads"
git commit -m "fix(filter): handle missing DVT files gracefully"
git commit -m "docs: update installation instructions for Windows"
git commit -m "test: add unit tests for KIC validation"
git commit -m "perf(database): optimize batch insert performance"

# Bad commit messages
git commit -m "fixed stuff"
git commit -m "updates"
git commit -m "work in progress"
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=kepler_downloader_dr25

# Run specific test file
pytest tests/test_downloader.py

# Run specific test
pytest tests/test_downloader.py::test_validate_kic
```

### Writing Tests

```python
# tests/test_downloader.py
import pytest
from kepler_downloader_dr25.downloader import validate_kic

def test_validate_kic_valid():
    """Test validation of valid KIC IDs."""
    assert validate_kic("006922244") == True
    assert validate_kic("007799349") == True

def test_validate_kic_invalid():
    """Test validation of invalid KIC IDs."""
    assert validate_kic("123") == False
    assert validate_kic("abc") == False
    assert validate_kic("") == False

@pytest.fixture
def sample_kic_list():
    """Fixture providing sample KIC IDs."""
    return ["006922244", "007799349", "011446443"]

def test_download_with_fixture(sample_kic_list):
    """Test download with sample KICs."""
    # Your test here
    pass
```

### Test Coverage

Aim for at least 80% test coverage for new code:

```bash
# Generate coverage report
pytest --cov=kepler_downloader_dr25 --cov-report=html

# View report
open htmlcov/index.html
```

## Submitting Changes

### Pull Request Process

1. **Update your fork**
   ```bash
   git remote add upstream https://github.com/akira921x/Kepler-Downloader-DR25.git
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Run tests
   pytest
   
   # Check code style
   flake8
   black --check .
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Go to GitHub and create a PR from your branch
   - Fill out the PR template completely
   - Link any related issues

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Updated existing tests

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

## Reporting Issues

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Check the documentation** for answers
3. **Verify your environment** meets requirements

### Issue Template

```markdown
## Description
Clear description of the issue

## To Reproduce
1. Step one
2. Step two
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.9.7]
- Package version: [e.g., 1.1.7]
- Redis version: [e.g., 6.2.6]

## Additional Context
Any other relevant information
```

## Questions?

If you have questions:

1. Check the [documentation](README.md)
2. Search [existing issues](https://github.com/akira921x/Kepler-Downloader-DR25/issues)
3. Ask in a [new issue](https://github.com/akira921x/Kepler-Downloader-DR25/issues/new)

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

Thank you for contributing to Kepler-Downloader-DR25! Your efforts help make this tool better for the entire astronomical research community.