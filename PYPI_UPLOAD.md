# How to Upload to PyPI

## Prerequisites

1. Create a PyPI account at https://pypi.org/account/register/
2. Verify your email address
3. Generate an API token:
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token
   - Save the token securely (starts with `pypi-`)

## Method 1: Using API Token (Recommended)

```bash
# Upload using API token
python3 -m twine upload dist/* --username __token__ --password <YOUR-API-TOKEN>

# Example:
python3 -m twine upload dist/* --username __token__ --password pypi-AgEIcHlwaS5vcmcCJGYwNzQ4...
```

## Method 2: Create .pypirc File

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE
```

Then upload:
```bash
python3 -m twine upload dist/*
```

## Method 3: Interactive Login

```bash
# This will prompt for username and password
python3 -m twine upload dist/*

# When prompted:
# Username: __token__
# Password: <paste your PyPI API token>
```

## Test with TestPyPI First (Optional)

1. Create TestPyPI account: https://test.pypi.org/account/register/
2. Upload to TestPyPI:
   ```bash
   python3 -m twine upload --repository testpypi dist/*
   ```
3. Test installation:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ kepler-downloader-dr25
   ```

## After Upload

Once uploaded successfully, your package will be available at:
- https://pypi.org/project/kepler-downloader-dr25/

Users can install with:
```bash
pip install kepler-downloader-dr25
```

## Files to Upload

Your distribution files are ready:
- `dist/kepler_downloader_dr25-1.0.0.tar.gz` (source distribution)
- `dist/kepler_downloader_dr25-1.0.0-py3-none-any.whl` (wheel)

## Troubleshooting

If you get "403 Forbidden":
- Package name might be taken
- API token might not have upload permissions
- You might not be the package owner

If you get "400 Bad Request":
- Package version already exists (bump version in setup.py)
- Package metadata might be invalid