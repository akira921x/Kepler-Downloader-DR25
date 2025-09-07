# GitHub Actions Workflow Management Guide

## Managing Workflow Run History

GitHub Actions workflow runs cannot be deleted manually, but there are several ways to manage and filter them effectively.

## Retention Settings

### Default Retention
- Public repositories: 90 days
- Private repositories: 90 days (can be customized)

### How to Adjust Retention Period
1. Go to **Settings** → **Actions** → **General**
2. Under **"Artifact and log retention"**
3. Set desired retention period (1-90 days)
4. Click **Save**

**Note**: Shorter retention periods help keep the Actions tab cleaner but may lose historical data needed for debugging.

## Filtering Workflow Runs

### Using the GitHub UI

#### View Only Successful Runs
https://github.com/akira921x/Kepler-Downloader-DR25/actions?query=is%3Asuccess

#### View Only Failed Runs
https://github.com/akira921x/Kepler-Downloader-DR25/actions?query=is%3Afailure

#### View Specific Workflow
https://github.com/akira921x/Kepler-Downloader-DR25/actions/workflows/ci.yml

#### Filter by Branch
https://github.com/akira921x/Kepler-Downloader-DR25/actions?query=branch%3Amain

### Using GitHub CLI

```bash
# List only successful runs
gh run list --repo akira921x/Kepler-Downloader-DR25 --status success

# List only failed runs
gh run list --repo akira921x/Kepler-Downloader-DR25 --status failure

# List runs for specific workflow
gh run list --repo akira921x/Kepler-Downloader-DR25 --workflow ci.yml

# List runs for specific branch
gh run list --repo akira921x/Kepler-Downloader-DR25 --branch main
```

## Workflow Status Badges

The README includes status badges that show the current state:

```markdown
[![CI Status](https://github.com/akira921x/Kepler-Downloader-DR25/actions/workflows/ci.yml/badge.svg)](https://github.com/akira921x/Kepler-Downloader-DR25/actions/workflows/ci.yml)
```

This badge automatically updates to show:
- ✅ **Passing** (green) - All tests successful
- ❌ **Failing** (red) - Tests failed
- ⚪ **No status** (grey) - No recent runs

## Best Practices

### 1. Focus on Recent Runs
The most recent runs are usually the most relevant. Old failed runs from development/debugging are less important once issues are resolved.

### 2. Use Branch Protection
Set up branch protection rules to prevent merging if CI fails:
1. Go to **Settings** → **Branches**
2. Add rule for `main` branch
3. Enable **"Require status checks to pass before merging"**
4. Select required workflows

### 3. Monitor Success Rate
Use the cleanup workflow to track success rates:
```bash
# Manual trigger of cleanup workflow
gh workflow run cleanup.yml --repo akira921x/Kepler-Downloader-DR25
```

### 4. Archive Important Logs
If you need to keep specific workflow logs:
```bash
# Download logs for a specific run
gh run download <run-id> --repo akira921x/Kepler-Downloader-DR25
```

## Understanding Workflow History

### Why Can't Runs Be Deleted?
GitHub maintains workflow run history for:
- **Audit trail**: Track who triggered what and when
- **Debugging**: Historical data helps identify patterns
- **Compliance**: Some organizations require activity logs
- **Transparency**: Public projects benefit from visible CI/CD history

### What Gets Cleaned Automatically?
After the retention period:
- Workflow run logs are deleted
- Artifacts are removed
- The run entry remains but without detailed logs

## Cleanup Workflow

A cleanup workflow runs weekly to provide statistics:
- Located at `.github/workflows/cleanup.yml`
- Runs every Sunday at 00:00 UTC
- Provides success/failure statistics
- Can be manually triggered

## Quick Links

- [All Workflows](https://github.com/akira921x/Kepler-Downloader-DR25/actions)
- [CI Workflow](https://github.com/akira921x/Kepler-Downloader-DR25/actions/workflows/ci.yml)
- [Successful Runs Only](https://github.com/akira921x/Kepler-Downloader-DR25/actions?query=is%3Asuccess)
- [Latest Main Branch](https://github.com/akira921x/Kepler-Downloader-DR25/actions?query=branch%3Amain+is%3Asuccess)