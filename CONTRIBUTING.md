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

## Tri-Perimeter Contribution Framework (TPCF)

This project uses a **graduated trust model** with three contribution perimeters. See [MAINTAINERS.md](MAINTAINERS.md) for full details.

### Perimeter 3: Community Sandbox (You Are Here!)

**Everyone starts here.** Open to all contributors.

**Access**: Fork-based contributions, public issues/discussions

**What you can do**:
- Report bugs and request features
- Submit pull requests (require review)
- Fix documentation
- Participate in discussions
- Help other community members

**Path forward**: After 3+ months and 10+ merged PRs, you can be nominated for Perimeter 2 (Trusted Contributor).

### Perimeter 2: Trusted Contributors

**Regular contributors with proven track record.**

**Access**: Write access to development branches, auto-approved CI/CD

**Requirements**:
- 3+ months of active contribution
- 10+ merged pull requests
- Demonstrated code quality
- Approval from 2+ core maintainers

### Perimeter 1: Core Maintainers

**Project leadership.**

**Access**: Write access to main branch, voting rights

**Requirements**:
- 6+ months as Trusted Contributor
- Deep expertise in component/area
- Leadership and mentoring
- Unanimous approval from existing core

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
