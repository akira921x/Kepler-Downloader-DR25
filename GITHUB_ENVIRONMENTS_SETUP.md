# GitHub Environments Setup Guide

This guide explains how to create and configure GitHub Environments for secure PyPI publishing.

## Why Use Environments?

GitHub Environments provide:
- **Protection rules** - Require reviews before deployment
- **Deployment history** - Track all deployments
- **Environment secrets** - Separate secrets per environment
- **Access control** - Restrict who can deploy

## Required Environments

We need to create two environments:

1. **`pypi`** - For production PyPI releases
2. **`testpypi`** - For TestPyPI testing

## Setup Instructions

### Step 1: Navigate to Settings

1. Go to your repository: https://github.com/akira921x/Kepler-Downloader-DR25
2. Click **Settings** tab
3. In the left sidebar, click **Environments**

### Step 2: Create "pypi" Environment

1. Click **New environment**
2. Name: `pypi`
3. Click **Configure environment**
4. Configure these settings:

   **Environment URL:**
   ```
   https://pypi.org/project/kepler-downloader-dr25/
   ```

   **Protection Rules (Optional but Recommended):**
   - ✅ Required reviewers: Add yourself or team members
   - ✅ Wait timer: 5 minutes (gives time to cancel if needed)
   - ✅ Deployment branches: Only from `main` branch

5. Click **Save protection rules**

### Step 3: Create "testpypi" Environment

1. Click **New environment**
2. Name: `testpypi`
3. Click **Configure environment**
4. Configure these settings:

   **Environment URL:**
   ```
   https://test.pypi.org/project/kepler-downloader-dr25/
   ```

   **Protection Rules (Less Strict):**
   - ⬜ Required reviewers: None (for easier testing)
   - ⬜ Wait timer: None
   - ✅ Deployment branches: `main` and `develop` branches

5. Click **Save protection rules**

## Updating PyPI Trusted Publishing

After creating the environments, update your PyPI settings:

### For PyPI (Production)

1. Go to: https://pypi.org/manage/account/publishing/
2. Add/Edit publisher with:
   - **Repository**: `akira921x/Kepler-Downloader-DR25`
   - **Workflow**: `publish-to-pypi.yml`
   - **Environment**: `pypi` ← Add this!

### For TestPyPI

1. Go to: https://test.pypi.org/manage/account/publishing/
2. Add/Edit publisher with:
   - **Repository**: `akira921x/Kepler-Downloader-DR25`
   - **Workflow**: `publish-to-testpypi.yml`
   - **Environment**: `testpypi` ← Add this!

## Workflow Configuration

Our workflows are already configured to use environments:

**publish-to-pypi.yml:**
```yaml
environment:
  name: pypi
  url: https://pypi.org/project/kepler-downloader-dr25/
```

**publish-to-testpypi.yml:**
```yaml
environment:
  name: testpypi
  url: https://test.pypi.org/project/kepler-downloader-dr25/
```

## Testing the Setup

### Test with TestPyPI First

1. Make a small change to the code
2. Push to main branch
3. Check Actions tab: https://github.com/akira921x/Kepler-Downloader-DR25/actions
4. Watch the "Publish to TestPyPI" workflow
5. If using protection rules, approve the deployment

### Production Release

1. Create a new release: https://github.com/akira921x/Kepler-Downloader-DR25/releases/new
2. The workflow will wait for approval (if configured)
3. Once approved, it publishes to PyPI

## Environment Secrets (Optional)

If you prefer using API tokens instead of Trusted Publishing:

1. Go to Environment settings
2. Click **Add secret**
3. Add `PYPI_API_TOKEN` with your PyPI token
4. Update workflow to use: `${{ secrets.PYPI_API_TOKEN }}`

## Benefits of This Setup

1. **Safety**: Can't accidentally publish to production
2. **Audit Trail**: All deployments are logged
3. **Team Workflow**: Require reviews for production releases
4. **Rollback**: Can see deployment history
5. **Security**: Environments + Trusted Publishing = Maximum security

## Troubleshooting

### "Environment not found"
- Ensure environment name matches exactly (case-sensitive)
- Check that environment is created in repository settings

### "Waiting for approval"
- Check repository Settings > Environments
- Look for pending approval requests
- Adjust protection rules if too restrictive

### "Deployment failed"
- Check Actions logs for details
- Verify PyPI Trusted Publishing settings
- Ensure environment name matches in both GitHub and PyPI