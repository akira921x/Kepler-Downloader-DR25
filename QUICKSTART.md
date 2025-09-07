# Quickstart: Kepler-Downloader-DR25

A high-performance toolkit for downloading **NASA Kepler Space Telescope** data from the **Mikulski Archive for Space Telescopes (MAST)**. This tool accesses the final Data Release 25 (DR25) - the most complete processing of Kepler's revolutionary exoplanet discovery data.

**Key Features:**
- ⚡ 5.5x faster than traditional bulk downloads
- 🔄 Automatic retry and recovery mechanisms
- 📊 99.9% success rate on 17,000+ KIC downloads
- 🤖 ML-ready formats (ExoMiner/AstroNet compatible)
- 🛡️ Zero database corruption with Redis buffering

**Data Source**: NASA/MAST at Space Telescope Science Institute (STScI)  
**Archive**: https://archive.stsci.edu/kepler/

## Main Download Workflow

### 1. Setup Redis (Recommended)

Redis prevents database corruption and improves performance:

```bash
# Quick setup - Choose ONE option:

# Option A: macOS with Homebrew
brew install redis && brew services start redis

# Option B: Ubuntu/Debian  
sudo apt install redis-server && sudo systemctl start redis

# Option C: Docker (no install needed)
docker run -d -p 6379:6379 --name redis-kepler redis:latest

# Verify Redis is running
redis-cli ping  # Should return "PONG"
```

### 2. Install Python Dependencies

```bash
cd /path/to/your/Kepler-Downloader-DR25
pip install -r requirements.txt
```

### 3. Download Data

#### Option A: ExoMiner Format with DVT Validation (Default)
```bash
# Download with ExoMiner structure and DVT filtering (default)
python get-kepler-dr25.py input/your_kics.csv

# Or use sample data
python get-kepler-dr25.py input_samples/cumulative_koi_2025.09.06_13.27.56.csv

# Backup KICs without DVT instead of deleting
python get-kepler-dr25.py input_samples/cumulative_koi_2025.09.06_13.27.56.csv --backup-no-dvt
```

#### Option B: Standard MAST Format
```bash
# Download with Standard MAST structure (no DVT requirement)
python get-kepler-dr25.py input/your_kics.csv --no-exominer
```

### 4. Filter Existing Data

The universal filter script can process any CSV and handle mode conversions:

```bash
# Filter existing job with KOI data
python filter-get-kepler-dr25.py \
  --input-csv input_samples/cumulative_koi_2025.09.06_13.27.56.csv \
  --source-job kepler_downloads/job-20250906_020543

# Convert from Standard to ExoMiner format (ExoMiner is default)
python filter-get-kepler-dr25.py \
  --input-csv input/kics.csv \
  --source-job kepler_downloads/standard_job \
  --force-mode  # Required for mode conversion
```

### 5. Monitor Progress

```bash
# Watch real-time download progress
tail -f kepler_downloads/job-*/download.log

# Check downloaded files (Standard format)
find kepler_downloads/job-*/mastDownload -name "*.fits" | wc -l

# Check downloaded files (ExoMiner format)  
find kepler_downloads/job-*/Kepler -name "*.fits" | wc -l

# View health report
cat kepler_downloads/job-*/health_check_report.txt
```

### 6. Results & Health Check

Each run creates a unique job directory:

```
kepler_downloads/job-YYYYMMDD_HHMMSS/
├── download_records.db          # SQLite database with all records
├── health_check_report.txt      # Comprehensive analysis
├── reports/                     # DVT filtering and other reports
│   ├── dvt_filter_report.txt   # ExoMiner DVT analysis
│   └── removed_kics.csv        # KICs removed for no DVT
└── [Data directories]          # Based on mode (Kepler/ or mastDownload/)
```

## Mode Detection & Compatibility

The filter script automatically detects and handles different modes:

### ExoMiner Mode (Default)
- Structure: `Kepler/XXXX/XXXXXXXXX/`
- **Requires DVT files** for each KIC
- Downloads LLC and DVT files
- Optimized for machine learning
- Default mode for both scripts

### Standard Mode
- Structure: `mastDownload/Kepler/kplr*_lc/`
- Downloads LLC and DVT files
- No DVT requirement
- MAST's default organization
- Use `--no-exominer` flag to enable

### Mode Compatibility Check
```bash
# Check job mode (will be shown in health report)
python filter-get-kepler-dr25.py \
  --input-csv input/kics.csv \
  --source-job kepler_downloads/job-20250906 \
  --verbose  # Shows detailed mode detection

# Force mode conversion if needed
python filter-get-kepler-dr25.py \
  --input-csv input/kics.csv \
  --source-job kepler_downloads/standard_job \
  --force-mode  # Required when modes don't match
```

## DVT Filtering (ExoMiner Only)

DVT (Data Validation) files are required for ExoMiner:

### During Download
```bash
# Strict mode - skip KICs without DVT immediately
python get-kepler-dr25.py input/kics.csv --strict-dvt

# Backup no-DVT KICs instead of deleting
python get-kepler-dr25.py input/kics.csv --backup-no-dvt
```

### During Filtering
```bash
# Disable DVT validation (not recommended for ExoMiner)
python filter-get-kepler-dr25.py \
  --input-csv input/kics.csv \
  --source-job kepler_downloads/job-20250906 \
  --no-validate-dvt
```

## Common Workflows

### Workflow 1: Download KOI Data for ExoMiner
```bash
# Download KOI data in ExoMiner format with DVT validation (default)
python get-kepler-dr25.py input_samples/cumulative_koi_2025.09.06_13.27.56.csv \
  --backup-no-dvt \
  --workers 8

# Check DVT coverage
cat kepler_downloads/job-*/reports/dvt_filter_report.txt
```

### Workflow 2: Filter TCE to KOI Only
```bash
# If you already downloaded TCE data, extract KOI subset
python filter-get-kepler-dr25.py \
  --input-csv input_samples/cumulative_koi_2025.09.06_13.27.56.csv \
  --source-job kepler_downloads/job-with-tce-data

# Result: New job with only KOI data in ExoMiner format
```

### Workflow 3: Convert Standard to ExoMiner
```bash
# Convert existing Standard format job to ExoMiner
python filter-get-kepler-dr25.py \
  --input-csv input/all_kics.csv \
  --source-job kepler_downloads/standard_job \
  --force-mode \
  --no-download-missing  # Skip downloading missing KICs
```

### Workflow 4: Rebuild Database from Filesystem
```bash
# If database is corrupted or missing, rebuild from filesystem
python util/rebuild_database.py kepler_downloads/job-20250907_015817

# This will scan all files and recreate the database
```

### Workflow 5: Check for Missing KICs
```bash
# Compare your input CSV with what was actually downloaded
python util/check_missing_kics.py input/target.csv kepler_downloads/job-20250907_015817

# Creates: missing_kics_job-20250907_015817.csv with any missing KICs
```

### Workflow 6: Generate Job Statistics
```bash
# Get comprehensive statistics for a completed job
python util/generate_stats.py kepler_downloads/job-20250907_015817

# Export to CSV for analysis
python util/generate_stats.py kepler_downloads/job-20250907_015817 --export job_stats.csv
```

## Performance Tips

1. **Use Redis** for optimal database performance
2. **Increase workers** for faster downloads: `--workers 8`
3. **Use larger batches**: `--batch-size 100`
4. **ExoMiner strict mode**: Use `--strict-dvt` to skip no-DVT KICs early
5. **Run during off-peak hours** for better MAST response

## Common Issues

### Redis Not Running?
```bash
redis-cli ping  # Should return "PONG"
brew services start redis  # macOS
sudo systemctl start redis  # Linux
```

### Database Shows All Zeros?
This was a known bug (missing conn.commit()) that has been fixed. If you have old downloads:
```bash
# Rebuild the database from filesystem
python util/rebuild_database.py kepler_downloads/job-YYYYMMDD_HHMMSS
```

### Mode Incompatibility?
- Check health report for details
- Use `--force-mode` to override (use cautiously)
- Consider target mode requirements

### DVT Missing (ExoMiner)?
- Some KICs don't have DVT files in MAST
- Use `--backup-no-dvt` to preserve data
- Consider Standard mode for analysis

### Downloads Failing?
- Check network connectivity
- Verify KIC exists in MAST
- Review health report for errors
- Retry with `--retry-failed`

## Database Queries

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('kepler_downloads/job-*/download_records.db')

# Check success rates
df = pd.read_sql_query("SELECT success, COUNT(*) FROM download_records GROUP BY success", conn)
print(df)

# Find KICs with DVT
df = pd.read_sql_query("SELECT COUNT(*) FROM download_records WHERE has_dvt = 1", conn)
print(df)

# Check removed KICs (ExoMiner)
df = pd.read_sql_query("SELECT * FROM removed_kics LIMIT 10", conn)
print(df)
```

## Monitoring Active Downloads

```bash
# Check download progress
ps aux | grep get-kepler-dr25.py

# View real-time logs (if available)
tail -f kepler_downloads/job-*/download.log

# Check database records during download
sqlite3 kepler_downloads/job-*/download_records.db \
  "SELECT COUNT(*) FROM download_records WHERE success=1"

# Monitor Redis buffer (during download)
redis-cli
> DBSIZE  # Shows number of keys
> KEYS job-*  # Lists active job keys
> EXIT
```

## Quick Reference

### File Formats
- **LLC files**: `*_llc.fits` - Light curve time series data
- **DVT files**: `*_dvt.fits` - Data validation (required for ExoMiner)
- **DVR files**: `*_dvr.pdf` - Data validation reports (PDF)

### Directory Structures
- **ExoMiner**: `Kepler/XXXX/XXXXXXXXX/*.fits`
- **Standard**: `mastDownload/Kepler/kplr*_lc/*.fits`

### Key Parameters
- **Workers**: More workers = faster downloads (default: 4, max recommended: 8)
- **Batch size**: Larger batches = fewer database writes (default: 50)
- **Redis**: Required for reliability, prevents database corruption

## Need Help?

- **Full documentation**: See [README.md](README.md)
- **Version history**: See [CHANGELOG.md](CHANGELOG.md) 
- **Debug logs**: Check `kepler_downloads/job-*/reports/`
- **Health reports**: Review `kepler_downloads/job-*/health_check_report.txt`
- **Issues**: Report at https://github.com/yourusername/Kepler-Downloader-DR25/issues

## Data Attribution

When using downloaded Kepler data, please cite:
- **Kepler Mission**: Borucki et al. (2010) Science, 327, 977
- **NASA Acknowledgment**: "This research has made use of the NASA Exoplanet Archive, operated by Caltech under contract with NASA."

All Kepler data is in the public domain. See README.md for complete citation guidelines.