# Contributing to Social Media Polygraph

Thank you for your interest in contributing! We welcome contributions from the community.

## Code of Conduct

Please be respectful and considerate in all interactions. We're building this together.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/hyperpolymath/social-media-polygraph/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, versions, etc.)
   - Screenshots if applicable

### Suggesting Features

1. Check [Discussions](https://github.com/hyperpolymath/social-media-polygraph/discussions) for similar ideas
2. Create a new discussion or issue explaining:
   - The problem you're trying to solve
   - Your proposed solution
   - Any alternatives you've considered

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Write or update tests
5. Ensure all tests pass: `poetry run pytest` (backend) or `npm test` (frontend)
6. Format your code:
   - Backend: `poetry run black app tests && poetry run ruff check app tests`
   - Frontend: `npm run lint`
7. Commit with clear messages: `git commit -m "Add feature: description"`
8. Push to your fork: `git push origin feature/my-feature`
9. Open a Pull Request

### Pull Request Guidelines

- Keep PRs focused on a single feature/fix
- Update documentation if needed
- Add tests for new functionality
- Ensure CI passes
- Link related issues

## Development Setup

See [README.md](README.md) for setup instructions.

### Backend Development

```bash
cd backend
poetry install
poetry run pytest
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## Code Style

### Python

- Follow PEP 8
- Use Black for formatting
- Use type hints
- Write docstrings for functions/classes

### TypeScript/React

- Follow Airbnb style guide
- Use TypeScript strictly
- Functional components with hooks
- Proper prop typing

## Testing

- Write unit tests for new functions
- Write integration tests for API endpoints
- Maintain >80% code coverage
- Test edge cases

## Commit Messages

Use conventional commits:

```
feat: add new feature
fix: fix bug
docs: update documentation
style: formatting changes
refactor: code refactoring
test: add tests
chore: maintenance tasks
```

## Questions?

- Open a [Discussion](https://github.com/hyperpolymath/social-media-polygraph/discussions)
- Join our community chat (if available)

Thank you for contributing!
