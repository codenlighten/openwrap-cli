# Contributing to LumenAI CLI

Thank you for your interest in contributing!

## Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Login to LumenAI: `python lumen_cli.py login`
4. Run tests: `python test_suite.py`

## Project Structure

```
lumen-greg/
├── lumen_cli.py              # Main CLI application
├── lumen_sdk.py              # Python SDK for programmatic access
├── example_*.py              # Example integrations
├── test_suite.py             # Automated tests
├── setup.py                  # Package configuration
└── docs/                     # Documentation
```

## Making Changes

### Adding New CLI Commands

1. Add method to `LumenCLI` class in `lumen_cli.py`
2. Add argument parser in `main()` function
3. Update README.md with usage
4. Test manually and add test case

### Adding SDK Features

1. Add method to `LumenClient` class in `lumen_sdk.py`
2. Include docstring with parameters and return type
3. Add example usage in SDK docstring
4. Create example file if needed

### Testing

Run the test suite before submitting:
```bash
python test_suite.py
```

Test your changes with real API calls:
```bash
python lumen_cli.py query "test message"
```

## Code Style

- Follow PEP 8
- Use type hints where appropriate
- Include docstrings for public methods
- Keep functions focused and single-purpose

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Update documentation
6. Submit pull request with clear description

## Reporting Issues

Include:
- Python version
- OS
- Steps to reproduce
- Expected vs actual behavior
- Error messages

## Questions?

Open an issue for discussion before making major changes.

## License

By contributing, you agree your code will be licensed under the MIT License.
