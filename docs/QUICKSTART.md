# Quick Start Guide

## Installation

### From PyPI (Recommended)
```bash
pip install kepler-downloader-dr25
```

### From Source
```bash
git clone https://github.com/akira921x/Kepler-Downloader-DR25.git
cd Kepler-Downloader-DR25
pip install -e .
```

## Basic Usage

### 1. Prepare Input CSV
Create a CSV file with KIC IDs (Kepler Input Catalog numbers):

```csv
kepid
757450
892772
1161345
1432214
```

### 2. Download Data

#### ExoMiner Format (Default - Recommended for ML)
```bash
kepler-download input.csv --workers 4
```

#### Standard MAST Format
```bash
kepler-download input.csv --no-exominer --workers 4
```

### 3. Filter Existing Data
Extract a subset from a previous download:

```bash
kepler-filter --input-csv subset.csv --source-job kepler_downloads/job-20250907_015817
```

## Key Features

### Parallel Downloads
- Use `--workers` to control parallelism (default: 4)
- Typical speed: 15-20 KICs per minute

### Redis Support (Optional)
For improved reliability with large datasets:

```bash
# Start Redis
redis-server

# Run download with Redis buffering
kepler-download input.csv --workers 8
```

### DVT File Filtering
ExoMiner mode automatically includes DVT (Data Validation) files:

```bash
# Include only KICs with DVT files
kepler-download input.csv --exominer

# Remove KICs without DVT after download
kepler-download input.csv --exominer --remove-no-dvt
```

## Output Structure

### ExoMiner Format
```
kepler_downloads/
└── job-YYYYMMDD_HHMMSS/
    ├── Kepler/
    │   ├── 0007/
    │   │   └── 000757450/
    │   │       ├── kplr000757450-2009131105131_llc.fits
    │   │       └── kplr000757450-20141002224145_dvt.fits
    │   └── 0008/
    │       └── 000892772/
    │           └── *.fits
    ├── download_records.db
    └── health_check_report.txt
```

### Standard Format
```
kepler_downloads/
└── job-YYYYMMDD_HHMMSS/
    ├── mastDownload/
    │   └── Kepler/
    │       ├── kplr000757450_lc/
    │       │   └── *.fits
    │       └── kplr000757450_dv/
    │           └── *.fits
    ├── download_records.db
    └── health_check_report.txt
```

## Sample Datasets

The repository includes sample CSV files in `input_samples/`:

- **KOI (Kepler Objects of Interest)**: ~9,500 planetary candidates
- **TCE (Threshold Crossing Events)**: ~34,000 transit signals

```bash
# Download all KOI targets
kepler-download input_samples/cumulative_koi_2025.09.06_13.27.56.csv --workers 8

# Download all TCE targets  
kepler-download input_samples/q1_q17_dr25_tce_2025.09.06_13.29.19.csv --workers 8
```

## Monitoring Progress

### Console Output
The tool provides real-time progress updates:
```
Processing KICs... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:05:23
Successfully downloaded: 7141/7141 KICs
```

### Health Report
Check `health_check_report.txt` for detailed statistics:
- Download success rate
- File counts by type
- Total data size
- DVT coverage statistics

### Database Queries
Use SQLite to query download records:

```bash
sqlite3 kepler_downloads/job-*/download_records.db
```

```sql
-- Check successful downloads
SELECT COUNT(*) FROM download_records WHERE success = 1;

-- Find KICs with DVT files
SELECT kic FROM download_records WHERE has_dvt = 1;
```

## Troubleshooting

### Redis Connection Issues
```bash
# Check if Redis is running
redis-cli ping

# Start Redis on macOS
brew services start redis

# Start Redis on Linux  
sudo systemctl start redis

# Start Redis on Windows (WSL2)
wsl
sudo service redis-server start

# Or use Docker on Windows
docker run -d -p 6379:6379 redis
```

### Network Timeouts
Increase timeout and retry settings:
```bash
kepler-download input.csv --timeout 60 --max-retries 5
```

### Disk Space
Check available space before large downloads:
```bash
# Estimate: ~25 MB per KIC (average)
# 10,000 KICs ≈ 250 GB
df -h
```

## Advanced Usage

### Custom Output Directory
```bash
kepler-download input.csv --output-dir /path/to/storage
```

### Batch Processing
```bash
kepler-download input.csv --batch-size 100 --workers 8
```

### Force Mode Conversion
Convert between formats (use with caution):
```bash
kepler-filter --input-csv input.csv --source-job old_job --force-mode
```

## Performance Tips

1. **Use Redis** for datasets > 1,000 KICs
2. **Increase workers** for faster downloads (up to 8-10)
3. **Use ExoMiner format** for ML/AI applications
4. **Filter instead of re-downloading** when creating subsets
5. **Monitor disk space** - each KIC averages 25 MB

## Support

- GitHub Issues: https://github.com/akira921x/Kepler-Downloader-DR25/issues
- Documentation: https://github.com/akira921x/Kepler-Downloader-DR25/tree/main/docs