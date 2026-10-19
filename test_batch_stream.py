import itertools
import time
import sys
# pyrefly: ignore[missing-import]
from datasets import load_dataset

print("Initializing streaming dataset...", flush=True)
start_time = time.time()
ds = load_dataset("RunningPie/CLARIS_sampledataset", split="train", streaming=True)
print(f"Dataset initialized in {time.time() - start_time:.2f}s", flush=True)

print("Starting streaming slice of 5000 rows...", flush=True)
rows = []
for idx, item in enumerate(itertools.islice(ds, 5000)):
    rows.append(item)
    if (idx + 1) % 500 == 0:
        elapsed = time.time() - start_time
        print(f"Processed {idx + 1} items ({elapsed:.2f}s elapsed, {item.get('sign')}, seq: {item.get('sequence_id')}, frame: {item.get('frame')})", flush=True)

print(f"Finished processing {len(rows)} items in {time.time() - start_time:.2f}s", flush=True)
print(f"Sample row: {rows[0]}", flush=True)
