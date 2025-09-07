# PyPI Trusted Publishing Setup

This guide explains how to set up Trusted Publishing for automatic package deployment from GitHub Actions to PyPI.

## What is Trusted Publishing?

Trusted Publishing allows GitHub Actions to publish packages to PyPI without storing API tokens or passwords. It uses OpenID Connect (OIDC) for secure authentication.

## Setup Steps

### 1. PyPI Configuration

1. **Log in to PyPI**: https://pypi.org/account/login/
2. **Go to Publishing Settings**: https://pypi.org/manage/account/publishing/
3. **Add a new publisher** with these settings:

   - **PyPI Project Name**: `kepler-downloader-dr25`
   - **Owner**: `akira921x`
   - **Repository name**: `Kepler-Downloader-DR25`
   - **Workflow name**: `publish-to-pypi.yml`
   - **Environment name**: (leave blank)

### 2. TestPyPI Configuration (Optional)

1. **Log in to TestPyPI**: https://test.pypi.org/account/login/
2. **Go to Publishing Settings**: https://test.pypi.org/manage/account/publishing/
3. **Add a new publisher** with these settings:

   - **PyPI Project Name**: `kepler-downloader-dr25`
   - **Owner**: `akira921x`
   - **Repository name**: `Kepler-Downloader-DR25`
   - **Workflow name**: `publish-to-testpypi.yml`
   - **Environment name**: (leave blank)

## GitHub Workflows

We have two workflows configured:

### 1. `publish-to-pypi.yml`
- **Trigger**: On GitHub Release creation
- **Target**: PyPI (production)
- **File**: `.github/workflows/publish-to-pypi.yml`

### 2. `publish-to-testpypi.yml`
- **Trigger**: On push to main branch or manual trigger
- **Target**: TestPyPI (testing)
- **File**: `.github/workflows/publish-to-testpypi.yml`

## How to Use

### Publishing to TestPyPI

1. Push changes to main branch, OR
2. Manually trigger from GitHub Actions tab:
   - Go to: https://github.com/akira921x/Kepler-Downloader-DR25/actions
   - Select "Publish to TestPyPI"
   - Click "Run workflow"

### Publishing to PyPI

1. Create a new GitHub Release:
   - Go to: https://github.com/akira921x/Kepler-Downloader-DR25/releases/new
   - Create a new tag (e.g., `v1.0.1`)
   - Write release notes
   - Click "Publish release"
2. The workflow will automatically build and publish to PyPI

## Verification

After publishing, verify your package:

**For PyPI:**
```bash
pip install kepler-downloader-dr25
# Check at: https://pypi.org/project/kepler-downloader-dr25/
```

**For TestPyPI:**
```bash
pip install --index-url https://test.pypi.org/simple/ kepler-downloader-dr25
# Check at: https://test.pypi.org/project/kepler-downloader-dr25/
```

## Troubleshooting

### "Workflow name not found"
- Ensure the workflow file exists in `.github/workflows/`
- Filename must match exactly what you configured in PyPI

### "Publisher not found"
- Check that repository owner and name match exactly
- Ensure the workflow has `permissions: id-token: write`

### "Package already exists"
- For first-time publishing, package name must not exist on PyPI
- For updates, you must be the package owner or have permissions

## Benefits of Trusted Publishing

1. **No secrets management** - No API tokens to rotate or leak
2. **Automatic authentication** - GitHub Actions handles auth via OIDC
3. **Audit trail** - All publishes are linked to GitHub commits
4. **Security** - No long-lived credentials stored anywhere