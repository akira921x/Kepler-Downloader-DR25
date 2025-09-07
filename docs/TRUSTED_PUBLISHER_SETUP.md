# Setting up Trusted Publisher for PyPI

This guide explains how to configure Trusted Publisher for automated PyPI releases.

## Prerequisites

1. PyPI account with access to the package
2. GitHub repository with admin access
3. Package already exists on PyPI (for existing packages)

## Configuration Steps

### 1. PyPI Configuration

1. Log in to PyPI (https://pypi.org)
2. Navigate to your project page
3. Go to "Settings" → "Publishing"
4. Under "Trusted Publishers", click "Add a new publisher"
5. Configure the GitHub publisher:
   - Owner: `akira921x`
   - Repository name: `Kepler-Downloader-DR25`
   - Workflow name: `ci.yml`
   - Environment name: `pypi` (optional but recommended)

### 2. GitHub Repository Setup

#### Create PyPI Environment (Recommended)

1. Go to Settings → Environments
2. Click "New environment"
3. Name it `pypi`
4. Configure protection rules:
   - Required reviewers (optional)
   - Deployment branches: Only selected branches
   - Add rule: `refs/tags/v*` (only deploy on version tags)

#### Repository Secrets (Not needed with Trusted Publisher)

With Trusted Publisher, you don't need to store PyPI tokens as secrets.

### 3. Workflow Configuration

The CI workflow is already configured in `.github/workflows/ci.yml` with:

```yaml
publish:
  needs: [build, version-check]
  runs-on: ubuntu-latest
  if: startsWith(github.ref, 'refs/tags/v')
  environment:
    name: pypi
    url: https://pypi.org/p/kepler-downloader-dr25
  permissions:
    id-token: write  # Required for trusted publishing
  steps:
    - uses: pypa/gh-action-pypi-publish@release/v1
```

### 4. Creating a Release

1. Update version in `kepler_downloader_dr25/_version.py`
2. Commit the changes:
   ```bash
   git add kepler_downloader_dr25/_version.py
   git commit -m "Bump version to X.Y.Z"
   ```
3. Create and push a tag:
   ```bash
   git tag vX.Y.Z
   git push origin main
   git push origin vX.Y.Z
   ```
4. The CI workflow will automatically:
   - Run tests
   - Check version consistency
   - Build the package
   - Publish to PyPI using Trusted Publisher

## Benefits of Trusted Publisher

1. **No API tokens needed**: Eliminates token management and rotation
2. **Enhanced security**: Uses OIDC for authentication
3. **Verified badge**: Package gets a "Verified" badge on PyPI
4. **Audit trail**: All publishes are tracked in GitHub Actions

## Troubleshooting

### Common Issues

1. **Permission denied during publish**
   - Verify the Trusted Publisher is configured correctly on PyPI
   - Check the workflow name matches exactly
   - Ensure the environment name matches (if configured)

2. **Version mismatch**
   - The version-check job ensures tag matches package version
   - Update `_version.py` before creating the tag

3. **Workflow not triggering**
   - Ensure tag follows the pattern `vX.Y.Z`
   - Check branch protection rules don't block the workflow

## References

- [PyPI Trusted Publishers Documentation](https://docs.pypi.org/trusted-publishers/)
- [GitHub OIDC Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)