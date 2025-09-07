#!/usr/bin/env python3
"""
Compare training_set.csv with downloaded KICs to find any missing data
"""

import pandas as pd
import sqlite3
import sys
from pathlib import Path

def check_missing_kics():
    # Read training set
    training_csv = "input/training_set.csv"
    training_df = pd.read_csv(training_csv)
    training_kics = set(training_df['kepid'].astype(int))
    
    print(f"Training set KICs: {len(training_kics)}")
    
    # Connect to database
    db_path = "kepler_downloads/job-20250907_114458/download_records.db"
    if not Path(db_path).exists():
        print(f"Error: Database not found at {db_path}")
        sys.exit(1)
    
    conn = sqlite3.connect(db_path)
    
    # Get downloaded KICs
    downloaded_df = pd.read_sql_query(
        "SELECT DISTINCT kic FROM download_records WHERE success = 1",
        conn
    )
    downloaded_kics = set(downloaded_df['kic'].astype(int))
    
    print(f"Downloaded KICs: {len(downloaded_kics)}")
    
    # Find missing KICs
    missing_kics = training_kics - downloaded_kics
    extra_kics = downloaded_kics - training_kics
    
    print(f"\n{'='*60}")
    print("COMPARISON RESULTS")
    print('='*60)
    
    if missing_kics:
        print(f"\n⚠️  MISSING KICs from training set: {len(missing_kics)}")
        print("Missing KIC IDs:")
        for kic in sorted(missing_kics):
            # Check if it failed to download
            cursor = conn.cursor()
            cursor.execute(
                "SELECT error_message FROM download_records WHERE kic = ? AND success = 0",
                (kic,)
            )
            error = cursor.fetchone()
            if error:
                print(f"  {kic:09d} - Failed: {error[0]}")
            else:
                print(f"  {kic:09d} - Not attempted")
    else:
        print("\n✅ ALL training set KICs were successfully downloaded!")
    
    if extra_kics:
        print(f"\n📝 Extra KICs downloaded (not in training set): {len(extra_kics)}")
        if len(extra_kics) <= 10:
            print("Extra KIC IDs:")
            for kic in sorted(extra_kics):
                print(f"  {kic:09d}")
    
    # Get statistics for training set KICs
    print(f"\n{'='*60}")
    print("TRAINING SET STATISTICS")
    print('='*60)
    
    if downloaded_kics:
        # Get DVT statistics
        placeholders = ','.join('?' * len(downloaded_kics))
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN has_dvt = 1 THEN 1 ELSE 0 END) as with_dvt,
                SUM(files_downloaded) as total_files,
                SUM(llc_files) as llc_files,
                SUM(dvt_files) as dvt_files
            FROM download_records 
            WHERE kic IN ({placeholders}) AND success = 1
            """,
            list(downloaded_kics)
        )
        
        stats = cursor.fetchone()
        if stats:
            total, with_dvt, total_files, llc_files, dvt_files = stats
            print(f"Successfully downloaded: {total}")
            print(f"KICs with DVT files: {with_dvt} ({with_dvt/total*100:.1f}%)")
            print(f"Total files: {total_files:,}")
            print(f"LLC files: {llc_files:,}")
            print(f"DVT files: {dvt_files:,}")
    
    conn.close()
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    completeness = len(downloaded_kics & training_kics) / len(training_kics) * 100
    print(f"Training set completeness: {completeness:.2f}%")
    
    if completeness == 100:
        print("✅ Perfect match! All training set KICs are available.")
    elif completeness >= 99:
        print("✅ Excellent coverage! Nearly all training KICs are available.")
    elif completeness >= 95:
        print("⚠️  Good coverage, but some training KICs are missing.")
    else:
        print("❌ Significant gaps in training set coverage.")

if __name__ == "__main__":
    check_missing_kics()