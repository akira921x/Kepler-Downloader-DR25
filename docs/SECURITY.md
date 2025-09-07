# Security Policy and Supply Chain Verification

## Overview

This document outlines the security measures and supply chain verification processes implemented for the Kepler-Downloader-DR25 package.

## Security Features

### 1. Trusted Publishing with Attestations

- **Implementation**: PyPI Trusted Publisher via GitHub OIDC
- **Attestations**: PEP 740 compliant attestations automatically generated
- **Benefits**: 
  - No API tokens stored in repository
  - Cryptographic proof of package origin
  - Verified publisher badge on PyPI

### 2. Package Signing with Sigstore

- **Technology**: Sigstore/Cosign for keyless signing
- **Process**: Automatic signing on each release
- **Verification**: Public transparency log via Rekor
- **Files Generated**:
  - `.sig` - Detached signatures
  - `.crt` - Signing certificates
  - `.bundle` - Verification bundle

### 3. Software Bill of Materials (SBOM)

- **Format**: CycloneDX (JSON and XML)
- **Contents**: Complete dependency tree with versions
- **License Compliance**: Automated license checking
- **Updates**: Generated for each release

### 4. Continuous Security Scanning

- **Dependency Scanning**: Safety for known vulnerabilities
- **Code Scanning**: Bandit for security issues
- **Frequency**: On every push and pull request
- **Reports**: Available as CI artifacts

## Verification Instructions

### Verify Package Authenticity

#### 1. Check PyPI Attestations

```bash
# View attestations on PyPI package page
# https://pypi.org/project/kepler-downloader-dr25/
# Look for the "Verified" badge and attestation details
```

#### 2. Verify Sigstore Signatures

```bash
# Install sigstore
pip install sigstore

# Download package
pip download kepler-downloader-dr25 --no-deps

# Verify signature
python -m sigstore verify identity \
  --cert-identity "https://github.com/akira921x/Kepler-Downloader-DR25/.github/workflows/publish.yml@refs/tags/vX.Y.Z" \
  --cert-oidc-issuer "https://token.actions.githubusercontent.com" \
  kepler-downloader-dr25-X.Y.Z.tar.gz
```

#### 3. Verify Checksums

```bash
# Download SHA256SUMS.txt from GitHub release
curl -L https://github.com/akira921x/Kepler-Downloader-DR25/releases/download/vX.Y.Z/SHA256SUMS.txt -o SHA256SUMS.txt

# Verify checksum
sha256sum -c SHA256SUMS.txt
```

### Check Supply Chain Security

#### 1. Review SBOM

```bash
# Download SBOM from release artifacts
curl -L https://github.com/akira921x/Kepler-Downloader-DR25/releases/download/vX.Y.Z/sbom.json -o sbom.json

# Review dependencies
cat sbom.json | jq '.components'
```

#### 2. Scan for Vulnerabilities

```bash
# Install safety
pip install safety

# Check installed package
safety check --key YOUR_API_KEY
```

## Security Workflows

### Release Process

1. **Code Review**: All changes reviewed before merge
2. **CI Testing**: Automated tests on multiple platforms
3. **Security Scan**: Vulnerability scanning before release
4. **Build**: Clean build in isolated environment
5. **Sign**: Automatic signing with Sigstore
6. **Attest**: GitHub attestations generated
7. **Publish**: Trusted Publisher to PyPI
8. **Verify**: Post-release verification

### Incident Response

If you discover a security vulnerability:

1. **Do NOT** create a public issue
2. **Email**: Report to maintainers privately
3. **Include**: 
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Best Practices for Users

### Installation

```bash
# Always use pip with hash verification
pip install kepler-downloader-dr25 --require-hashes

# Or specify exact version
pip install kepler-downloader-dr25==1.2.0

# Verify installation
pip show kepler-downloader-dr25 --verbose
```

### Verification Checklist

- [ ] Check for "Verified" badge on PyPI
- [ ] Verify package signatures if high security needed
- [ ] Review SBOM for unexpected dependencies
- [ ] Run security scan on installed package
- [ ] Check GitHub release for checksums
- [ ] Monitor security advisories

## Automated Security Features

### GitHub Actions Workflows

1. **CI Pipeline** (`ci.yml`)
   - Linting and type checking
   - Multi-platform testing
   - Security vulnerability scanning
   - Build verification

2. **Publish Pipeline** (`publish.yml`)
   - Version consistency check
   - Trusted publishing with attestations
   - Multi-platform installation verification
   - GitHub release asset creation

3. **Sign & Verify Pipeline** (`sign-verify.yml`)
   - Sigstore signing
   - SBOM generation
   - Supply chain verification report
   - Artifact attestation

## Compliance

### Standards and Frameworks

- **PEP 740**: Attestations for Python packages
- **SLSA Level 3**: Build provenance and isolation
- **CycloneDX**: SBOM format standard
- **OpenSSF**: Best practices for open source security

### Security Badges

[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/YOUR_PROJECT_ID/badge)](https://bestpractices.coreinfrastructure.org/projects/YOUR_PROJECT_ID)
[![Security Scan](https://github.com/akira921x/Kepler-Downloader-DR25/actions/workflows/ci.yml/badge.svg)](https://github.com/akira921x/Kepler-Downloader-DR25/actions/workflows/ci.yml)

## Resources

- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [Sigstore Documentation](https://docs.sigstore.dev/)
- [GitHub Attestations](https://docs.github.com/en/actions/security-guides/using-artifact-attestations)
- [SLSA Framework](https://slsa.dev/)
- [CycloneDX Specification](https://cyclonedx.org/)

## Updates

This security policy is regularly reviewed and updated. Last update: 2024

For security concerns or questions, please contact the maintainers through GitHub issues (for non-sensitive matters) or via private communication for security vulnerabilities.