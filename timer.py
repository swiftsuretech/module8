"""
Timer - GPU vs CPU performance comparison helper
"""

import re

def summary():
    """Display a summary of GPU vs CPU inference times."""
    print("=" * 50)
    print("GPU vs CPU Performance Summary")
    print("=" * 50)
    
    results = []
    
    # Check each result file
    files = [
        ("/tmp/gpu_7.txt", "GPU", "7.png"),
        ("/tmp/gpu_8.txt", "GPU", "8.png"),
        ("/tmp/cpu_7.txt", "CPU", "7.png"),
    ]
    
    for filepath, device, image in files:
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            match = re.search(r'Time\s*:\s*([\d.]+)\s*seconds', content)
            if match:
                time_val = float(match.group(1))
                results.append((device, image, time_val))
                print(f"{device} with {image}: {time_val:.2f} seconds")
        except FileNotFoundError:
            pass
    
    # Calculate speedup if we have both GPU and CPU results for 7.png
    gpu_time = next((r[2] for r in results if r[0] == "GPU" and r[1] == "7.png"), None)
    cpu_time = next((r[2] for r in results if r[0] == "CPU" and r[1] == "7.png"), None)
    
    if gpu_time and cpu_time:
        print("-" * 50)
        speedup = cpu_time / gpu_time
        print(f"GPU is {speedup:.1f}x faster than CPU!")
    
    print("=" * 50)

