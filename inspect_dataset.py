from datasets import load_dataset
import sys

print("Connecting to RunningPie/CLARIS_sampledataset in streaming mode...")
try:
    ds = load_dataset("RunningPie/CLARIS_sampledataset", split="train", streaming=True)
except Exception as e:
    print(f"Error loading train split: {e}")
    try:
        ds = load_dataset("RunningPie/CLARIS_sampledataset", streaming=True)
        print("Available splits:", list(ds.keys()))
        split_name = list(ds.keys())[0]
        ds = ds[split_name]
    except Exception as e2:
        print(f"Error loading dataset: {e2}")
        sys.exit(1)

print("Inspecting first record...")
first_batch = []
for i, item in enumerate(ds):
    first_batch.append(item)
    if i >= 4:
        break

for i, item in enumerate(first_batch):
    print(f"Sample {i}: {item}")

print("\nStreaming to collect unique signs...")
unique_signs = set()
count = 0
for item in ds:
    count += 1
    sign = item.get("sign")
    if sign not in unique_signs:
        unique_signs.add(sign)
        print(f"Found new sign (#{len(unique_signs)}): '{sign}' at row {count}")
    if count % 100000 == 0:
        print(f"Streamed {count} rows... Unique signs so far: {len(unique_signs)}")

print(f"\nTotal rows scanned: {count}")
print(f"All unique signs ({len(unique_signs)}):")
print(sorted(list(unique_signs)))
