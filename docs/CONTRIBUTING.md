# Contributing to Quantum Safe TLS Proxy

We welcome contributions! Here are some guidelines to follow.

## Getting Started
1. **Fork the Repository**: Create a fork on GitHub.
2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/your-username/quantum-safe-tls-proxy.git
   cd quantum-safe-tls-proxy
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up Pre-commit Hooks**:
   ```bash
   pre-commit install
   ```

## Code Style
- Follow PEP 8 for Python code.
- Use consistent naming conventions (`snake_case` for variables, `CamelCase` for classes).
- Format code with `black` before submitting.

## Issue Tracking
- **Report Issues**: Open an issue for bugs or feature requests.
- **Project Roadmap**: Check the `ROADMAP.md` file for upcoming features.

## Submitting a Pull Request
1. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Run Automated Tests**:
   ```bash
   pytest --cov=src tests/
   ```
3. **Code Review Checklist**:
   - [ ] Code follows style guidelines
   - [ ] Tests have been added for new functionality
   - [ ] Documentation has been updated

4. **Create the Pull Request**: Push the branch and open a PR.

## Running Tests
Run tests with:
```bash
pytest
```

## Coding Style Guide
- Use `black` for formatting.
- Use `flake8` for linting.
