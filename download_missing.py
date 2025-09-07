#!/usr/bin/env python3
"""
Try to download the missing KICs from training set
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kepler_downloader_dr25.downloader import FastKeplerDownloader

def download_missing_kics():
    missing_kics = ['007032687', '008429668', '008953296', '009474483']
    
    print("Attempting to download missing KICs from training set...")
    print(f"Missing KICs: {missing_kics}")
    print("="*60)
    
    # Initialize downloader with existing job directory
    job_dir = "kepler_downloads/job-20250907_114458"
    downloader = FastKeplerDownloader(
        download_dir="kepler_downloads",
        job_id="job-20250907_114458_missing",
        max_workers=2,
        exominer_format=True,
        strict_dvt=False  # Don't require DVT files
    )
    
    # Try to download each missing KIC
    results = []
    for kic in missing_kics:
        print(f"\nAttempting to download KIC {kic}...")
        result = downloader.download_kic(kic)
        results.append(result)
        
        if result['success']:
            print(f"✅ Successfully downloaded KIC {kic}")
            print(f"   Files: {result['files_downloaded']}, Has DVT: {result['has_dvt']}")
        else:
            print(f"❌ Failed to download KIC {kic}")
            print(f"   Error: {result.get('error', 'Unknown error')}")
    
    # Summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"Total attempted: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print("\nFailed KICs:")
        for kic, result in zip(missing_kics, results):
            if not result['success']:
                print(f"  {kic}: {result.get('error', 'Unknown error')}")
    
    return results

if __name__ == "__main__":
    download_missing_kics()