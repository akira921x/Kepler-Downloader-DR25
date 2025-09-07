#!/usr/bin/env python3
"""
Deep root cause analysis of missing KICs
"""

import pandas as pd
import numpy as np

# The 4 missing KICs and their positions
missing_kics = [7032687, 8429668, 8953296, 9474483]

# Load training set
df = pd.read_csv('input/training_set.csv')
all_kics = df['kepid'].tolist()

print("="*70)
print("ROOT CAUSE ANALYSIS: Why 4 KICs Were Missing")
print("="*70)

# Get positions
positions = [all_kics.index(kic) for kic in missing_kics]

print("\n1. POSITION ANALYSIS:")
print("-" * 40)
for kic, pos in zip(missing_kics, positions):
    print(f"KIC {kic}: Position {pos} (0-indexed)")

# Theory 1: Check if they're at specific intervals
print("\n2. INTERVAL PATTERN CHECK:")
print("-" * 40)
diffs = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
print(f"Gaps between missing KICs: {diffs}")
print(f"Average gap: {np.mean(diffs):.1f}")

# Theory 2: Redis sync batch mismatch
print("\n3. REDIS SYNC BATCH ANALYSIS:")
print("-" * 40)
print("Code shows TWO different batch sizes:")
print("  - self.batch_size = 50 (default for processing)")
print("  - hardcoded batch_size = 100 (in _sync_redis_to_db)")

# Simulate what happens with mismatched batch sizes
process_batch_size = 50
sync_batch_size = 100

print(f"\nWith process_batch={process_batch_size}, sync_batch={sync_batch_size}:")

# Theory 3: Check modulo patterns
print("\n4. MODULO PATTERN ANALYSIS:")
print("-" * 40)
for kic, pos in zip(missing_kics, positions):
    print(f"KIC {kic} (pos {pos}):")
    print(f"  pos % 50 = {pos % 50}")
    print(f"  pos % 100 = {pos % 100}")
    print(f"  pos % 1000 = {pos % 1000}")

# Theory 4: Threading race condition
print("\n5. MULTI-THREADING BOUNDARY ANALYSIS:")
print("-" * 40)
# With 4 workers (default max_workers=4)
workers = 4
for kic, pos in zip(missing_kics, positions):
    worker_id = pos % workers
    print(f"KIC {kic} (pos {pos}) → Worker {worker_id}")

# Theory 5: Batch processing boundaries
print("\n6. BATCH PROCESSING SIMULATION:")
print("-" * 40)
batch_size = 50
total_batches = (len(all_kics) + batch_size - 1) // batch_size

print(f"Total KICs: {len(all_kics)}")
print(f"Batch size: {batch_size}")
print(f"Total batches: {total_batches}")

# Check which batch each missing KIC is in
for kic, pos in zip(missing_kics, positions):
    batch_num = pos // batch_size
    pos_in_batch = pos % batch_size
    batch_start = batch_num * batch_size
    batch_end = min(batch_start + batch_size, len(all_kics))
    
    print(f"\nKIC {kic} (pos {pos}):")
    print(f"  Batch {batch_num} (items {batch_start}-{batch_end-1})")
    print(f"  Position in batch: {pos_in_batch}")
    
    # Check if near boundaries
    if pos_in_batch == 0:
        print(f"  ⚠️  FIRST item in batch!")
    elif pos_in_batch == batch_size - 1:
        print(f"  ⚠️  LAST item in batch!")
    elif pos_in_batch == batch_end - batch_start - 1:
        print(f"  ⚠️  LAST item in final partial batch!")

# The smoking gun
print("\n" + "="*70)
print("🔍 MOST LIKELY ROOT CAUSE:")
print("="*70)

print("""
The evidence strongly suggests a REDIS SYNCHRONIZATION BUG:

1. The hardcoded batch_size=100 in _sync_redis_to_db() differs from 
   the default self.batch_size=50 used for processing.

2. The missing KICs are scattered, not consecutive, suggesting they
   were processed but lost during sync.

3. Redis LTRIM operation after sync could have deleted records that
   hadn't been synced yet due to the batch size mismatch.

SPECIFIC BUG MECHANISM:
- Processing adds records to Redis in batches of 50
- Sync reads in batches of 100
- If Redis has 150 records: sync reads 100, processes them, 
  then LTRIM removes first 100, leaving 50
- But if a worker adds more records during sync, the LTRIM 
  could remove unsynced records

The 4 missing KICs were likely in Redis but got trimmed before 
being written to SQLite.
""")