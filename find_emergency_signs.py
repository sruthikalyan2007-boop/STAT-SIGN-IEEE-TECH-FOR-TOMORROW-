import requests
import time

url = "https://huggingface.co/datasets/RunningPie/CLARIS_sampledataset/resolve/main/claris_curated_dataset.csv"
total_size = 5769622949

def get_sign_at(byte_pos):
    try:
        r = requests.get(url, headers={'Range': f'bytes={byte_pos}-{byte_pos+2000}'}, timeout=10)
        lines = r.text.split('\n')
        for line in lines[1:]:
            parts = line.split(',')
            if len(parts) >= 10:
                return parts[9].strip()
    except Exception as e:
        pass
    return None

def find_sign_offset(target_sign, low=0, high=total_size):
    for _ in range(35):
        mid = (low + high) // 2
        s = get_sign_at(mid)
        if s is None:
            high = mid
            continue
        if s < target_sign:
            low = mid
        else:
            high = mid
    return low

signs = ['arm', 'bad', 'cry', 'cut', 'fall', 'fireman', 'owie', 'police', 'sick', 'stuck']
print(f"Finding exact byte offsets for 10 emergency signs in {total_size / 1e9:.2f} GB dataset...", flush=True)

offsets = {}
for s in signs:
    t0 = time.time()
    pos = find_sign_offset(s)
    actual_sign = get_sign_at(pos + 5000)
    offsets[s] = pos
    print(f"Sign '{s}': offset {pos} ({pos/1024/1024:.1f} MB), verified: '{actual_sign}' in {time.time()-t0:.2f}s", flush=True)

print("\nAll offsets located:", offsets)
