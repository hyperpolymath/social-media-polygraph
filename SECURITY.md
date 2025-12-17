# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

### Preferred: Security Advisory

1. Go to the repository's Security tab
2. Click "Report a vulnerability"
3. Fill out the advisory form

### Alternative: Email

Send an email to the maintainers via [GitHub Security Advisories](https://github.com/hyperpolymath/social-media-polygraph/security/advisories/new) with:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### What to Expect

- **Response Time**: We aim to acknowledge receipt within 48 hours
- **Status Updates**: You will receive status updates at least every 5 business days
- **Disclosure Timeline**: We follow coordinated disclosure practices
  - We aim to release fixes within 90 days
  - We will work with you on disclosure timing
  - Public disclosure will be coordinated with you

### Security Response Process

1. **Triage** (Day 0-2): Acknowledge receipt, initial assessment
2. **Investigation** (Day 3-14): Reproduce, verify, assess impact
3. **Fix Development** (Day 15-60): Develop and test patch
4. **Review** (Day 61-75): Security review, testing
5. **Disclosure** (Day 76-90): Coordinated public disclosure

## Security Measures

This project implements multiple security layers:

### Application Security

- **Authentication**: JWT tokens with secure signing
- **Password Hashing**: bcrypt with appropriate work factor
- **Rate Limiting**: Protection against abuse and DoS
- **Input Validation**: Pydantic schemas for all inputs
- **CORS**: Properly configured cross-origin policies
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, etc.

### Infrastructure Security

- **Container Security**: Non-root users in containers
- **Secrets Management**: Environment variables, never committed
- **Database Security**: Parameterized queries (NoSQL), access controls
- **Network Security**: Minimal exposed ports
- **Dependency Scanning**: Automated vulnerability scanning in CI/CD

### Data Security

- **Encryption in Transit**: HTTPS/TLS for all connections
- **Encryption at Rest**: Database encryption (when configured)
- **Data Minimization**: Collect only necessary data
- **Privacy**: No selling or sharing of user data

## Known Security Considerations

### External Dependencies

This project depends on:
- **Fact-checking APIs**: Third-party services (validate their security)
- **NLP Models**: Pre-trained models (verify provenance)
- **Database Systems**: ArangoDB, XTDB, Dragonfly (keep updated)

### Attack Surface

- **API Endpoints**: Publicly accessible, protected by rate limiting and auth
- **User Input**: All claim text is untrusted, sanitized before processing
- **External Content**: URLs and social media content are untrusted
- **Browser Extension**: Runs with elevated permissions (regularly audited)

## Security Best Practices for Deployments

### Production Deployment

1. **Change All Default Secrets**
   - Generate strong SECRET_KEY
   - Generate strong JWT_SECRET_KEY
   - Use strong database passwords

2. **Enable HTTPS**
   - Use Let's Encrypt or commercial certificates
   - Force HTTPS redirects
   - Enable HSTS headers

3. **Configure Firewalls**
   - Limit exposed ports
   - Use VPC/private networks for databases
   - Enable fail2ban for SSH

4. **Regular Updates**
   - Keep dependencies updated
   - Monitor security advisories
   - Apply patches promptly

5. **Monitoring**
   - Enable audit logging
   - Monitor for suspicious activity
   - Set up alerts for anomalies

### Development Security

1. **Never commit secrets** to version control
2. **Use `.env` files** for local development only
3. **Review dependencies** before adding
4. **Run security scanners** (Trivy, Bandit, etc.)
5. **Enable pre-commit hooks** for secret scanning

## Security Compliance

- **OWASP Top 10**: Addressed common vulnerabilities
- **CWE/SANS Top 25**: Mitigations in place
- **GDPR**: Privacy-by-design principles (for EU deployments)
- **SOC 2** (optional): Security controls documented

## Bug Bounty Program

Currently, we do not have a formal bug bounty program. However, we appreciate security researchers who responsibly disclose vulnerabilities and will:

- Acknowledge contributions in our CHANGELOG
- Provide attribution in security advisories (with permission)
- Send thank-you notes and swag (when available)

## Hall of Fame

Security researchers who have responsibly disclosed vulnerabilities:

<!-- None yet - this is a new project -->

## Contact

- **Security Issues**: [GitHub Security Advisories](https://github.com/hyperpolymath/social-media-polygraph/security/advisories/new)
- **General Questions**: See CONTRIBUTING.md for community channels

## Attribution

This security policy is inspired by:
- [GitHub's Coordinated Disclosure Guidelines](https://docs.github.com/en/code-security/security-advisories)
- [OWASP Vulnerability Disclosure Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html)
