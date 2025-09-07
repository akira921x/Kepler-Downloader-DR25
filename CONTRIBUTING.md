# Contributing to Kepler-Downloader-DR25

Thank you for your interest in contributing to Kepler-Downloader-DR25! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

1. **Check existing issues** - Before creating a new issue, please check if it already exists.
2. **Use issue templates** - Use the provided templates for bug reports and feature requests.
3. **Provide details** - Include as much relevant information as possible:
   - Python version
   - Operating system
   - Error messages
   - Sample data to reproduce the issue

### Contributing Code

#### Getting Started

1. Fork the repository
2. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Set up your development environment:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Kepler-Downloader-DR25.git
   cd Kepler-Downloader-DR25
   pip install -r requirements.txt
   pip install -e .
   ```

#### Making Changes

1. **Follow existing code style**:
   - Use 4 spaces for indentation (no tabs)
   - Follow PEP 8 conventions
   - Add docstrings to functions and classes
   - Keep line length under 100 characters when possible

2. **Write clear commit messages**:
   - Use present tense ("Add feature" not "Added feature")
   - Use imperative mood ("Fix bug" not "Fixes bug")
   - Reference issues and pull requests when relevant

3. **Test your changes**:
   - Ensure existing tests pass
   - Add tests for new features
   - Test with different Python versions if possible

4. **Update documentation**:
   - Update README.md if adding new features
   - Update docstrings
   - Add examples if applicable

#### Submitting Pull Requests

1. **Before submitting**:
   - Rebase your branch on the latest main
   - Ensure all tests pass
   - Update documentation

2. **Pull Request Guidelines**:
   - Use a clear, descriptive title
   - Reference any related issues
   - Describe what changes you made and why
   - Include screenshots for UI changes

3. **Pull Request Template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   
   ## Testing
   - [ ] Tests pass locally
   - [ ] New tests added (if applicable)
   
   ## Checklist
   - [ ] Code follows project style
   - [ ] Documentation updated
   - [ ] No sensitive data included
   ```

### Areas for Contribution

We welcome contributions in these areas:

- **Bug fixes** - Help us squash bugs
- **Documentation** - Improve or translate documentation
- **Testing** - Add more test coverage
- **Performance** - Optimize download speeds or memory usage
- **Features** - Add new functionality (discuss first in issues)
- **Examples** - Add more usage examples

### Development Guidelines

#### Project Structure

```
Kepler-Downloader-DR25/
├── kepler_downloader_dr25/    # Main package
│   ├── downloader.py          # Core download functionality
│   ├── filter.py              # Filtering functionality
│   └── utils/                 # Utility functions
├── tests/                     # Test files
├── docs/                      # Documentation
└── examples/                  # Usage examples
```

#### Code Standards

- **Docstrings**: Use Google-style docstrings
- **Type hints**: Add type hints where appropriate
- **Error handling**: Use appropriate exception handling
- **Logging**: Use Python's logging module
- **Security**: Never commit credentials or sensitive data

#### Testing

Run tests locally:
```bash
python -m pytest tests/
```

### Community

- Be respectful and constructive
- Follow our [Code of Conduct](CODE_OF_CONDUCT.md)
- Help others in issues and discussions
- Share your use cases and experiences

### Questions?

If you have questions:
1. Check the [documentation](README.md)
2. Search existing [issues](https://github.com/akira921x/Kepler-Downloader-DR25/issues)
3. Open a new issue with the question label

## Recognition

Contributors will be recognized in:
- The project's contributors list
- Release notes for significant contributions

Thank you for helping make Kepler-Downloader-DR25 better!