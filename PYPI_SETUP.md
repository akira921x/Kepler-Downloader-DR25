# PyPI Trusted Publisher Setup Instructions

## IMPORTANT: Manual Configuration Required

The GitHub Actions workflow is configured but **will fail** until you complete the PyPI setup.

## Step-by-Step PyPI Configuration

### 1. Log in to PyPI
Visit: https://pypi.org/account/login/

### 2. Navigate to Project Settings
Go to: https://pypi.org/manage/project/kepler-downloader-dr25/settings/

### 3. Configure Publishing
Click on "Publishing" in the left sidebar

### 4. Add Trusted Publisher

Click "Add a new publisher" and configure **EXACTLY** as follows:

- **Publisher**: GitHub
- **Owner**: `akira921x`
- **Repository name**: `Kepler-Downloader-DR25`
- **Workflow name**: `publish.yml`
- **Environment name**: `production` (optional but recommended)

### 5. Save Settings
Click "Add" to save the configuration

## Verification

After configuration, the workflow will automatically:
1. Generate attestations (PEP 740)
2. Sign packages with Sigstore
3. Publish to PyPI with verified badge

## Testing with TestPyPI (Optional)

To test before production:

1. Create account at https://test.pypi.org
2. Create the same package name
3. Configure Trusted Publisher with same settings
4. Manually trigger workflow with TestPyPI option

## Troubleshooting

### Error: "invalid-publisher"
This means PyPI configuration is missing or incorrect. Double-check:
- Repository name matches exactly (case-sensitive)
- Workflow filename is `publish.yml` (not `ci.yml`)
- Environment name is `production` (if using environment)

### Error: "token request failed"
Check that GitHub environment "production" exists and is not blocking the deployment

## Current Workflow Claims

The workflow will present these claims to PyPI:
```
repository: akira921x/Kepler-Downloader-DR25
repository_owner: akira921x
workflow_ref: akira921x/Kepler-Downloader-DR25/.github/workflows/publish.yml@refs/tags/vX.Y.Z
environment: production
```

These must match your PyPI Trusted Publisher configuration exactly.