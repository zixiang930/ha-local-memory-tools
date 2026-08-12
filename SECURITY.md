# Security Policy

## Reporting a vulnerability

Please do not disclose exploitable security issues in a public issue.

When this repository is published, configure GitHub Private Vulnerability
Reporting and use it for security reports.

## Sensitive data

Do not paste Home Assistant secrets, access tokens, private configuration, or
stored memory contents into public issues.

The integration stores memory locally, but recalled text can be provided to the
configured LLM provider when a tool is called. Users are responsible for
understanding the privacy policy of their model provider.
