"""
Timer - GPU vs CPU performance comparison helper
"""

import re

def summary():
    """Display a summary of GPU vs CPU performance for both training and inference."""
    print("=" * 60)
    print("           GPU vs CPU Performance Summary")
    print("=" * 60)
    
    # Training results
    gpu_train_time = None
    cpu_train_time = None
    gpu_epochs = None
    cpu_epochs = None
    
    try:
        with open("/tmp/gpu_train.txt", 'r') as f:
            content = f.read()
        match = re.search(r'Time\s*:\s*([\d.]+)\s*seconds', content)
        if match:
            gpu_train_time = float(match.group(1))
        # Find highest epoch number
        epoch_matches = re.findall(r'Train Epoch:\s*(\d+)', content)
        if epoch_matches:
            gpu_epochs = max(int(e) for e in epoch_matches)
    except FileNotFoundError:
        pass
    
    try:
        with open("/tmp/cpu_train.txt", 'r') as f:
            content = f.read()
        match = re.search(r'Time\s*:\s*([\d.]+)\s*seconds', content)
        if match:
            cpu_train_time = float(match.group(1))
        epoch_matches = re.findall(r'Train Epoch:\s*(\d+)', content)
        if epoch_matches:
            cpu_epochs = max(int(e) for e in epoch_matches)
    except FileNotFoundError:
        pass
    
    # Determine epochs to display
    epochs = gpu_epochs or cpu_epochs or "?"
    print(f"\n📊 TRAINING ({epochs} epoch{'s' if epochs != 1 else ''} on MNIST - 60,000 images)")
    print("-" * 60)
    
    if gpu_train_time:
        print(f"  GPU Training:  {gpu_train_time:>7.1f} seconds")
    else:
        print("  GPU Training:  (not yet run)")
    
    if cpu_train_time:
        print(f"  CPU Training:  {cpu_train_time:>7.1f} seconds")
    else:
        print("  CPU Training:  (not yet run)")
    
    if gpu_train_time and cpu_train_time:
        speedup = cpu_train_time / gpu_train_time
        print(f"\n  ⚡ GPU is {speedup:.1f}x FASTER for training!")
    
    # Inference results
    print("\n📊 INFERENCE (single image prediction)")
    print("-" * 60)
    
    gpu_inf_time = None
    cpu_inf_time = None
    
    try:
        with open("/tmp/gpu_7.txt", 'r') as f:
            content = f.read()
        match = re.search(r'Time\s*:\s*([\d.]+)\s*seconds', content)
        if match:
            gpu_inf_time = float(match.group(1))
            print(f"  GPU Inference: {gpu_inf_time:>7.2f} seconds")
    except FileNotFoundError:
        print("  GPU Inference: (not yet run)")
    
    try:
        with open("/tmp/cpu_7.txt", 'r') as f:
            content = f.read()
        match = re.search(r'Time\s*:\s*([\d.]+)\s*seconds', content)
        if match:
            cpu_inf_time = float(match.group(1))
            print(f"  CPU Inference: {cpu_inf_time:>7.2f} seconds")
    except FileNotFoundError:
        print("  CPU Inference: (not yet run)")
    
    if gpu_inf_time and cpu_inf_time:
        if cpu_inf_time < gpu_inf_time:
            speedup = gpu_inf_time / cpu_inf_time
            print(f"\n  💡 CPU is {speedup:.1f}x faster for single inference")
            print("     (GPU overhead dominates for tiny workloads)")
        else:
            speedup = cpu_inf_time / gpu_inf_time
            print(f"\n  ⚡ GPU is {speedup:.1f}x faster for inference")
    
    # Summary
    print("\n" + "=" * 60)
    print("KEY TAKEAWAY:")
    print("-" * 60)
    if gpu_train_time and cpu_train_time:
        print(f"  • Training: GPU wins big ({cpu_train_time/gpu_train_time:.1f}x faster)")
        print("    → Large datasets benefit from GPU parallelism")
    if gpu_inf_time and cpu_inf_time and cpu_inf_time < gpu_inf_time:
        print(f"  • Inference: CPU faster for single images")
        print("    → GPU data transfer overhead exceeds compute time")
    print("=" * 60)
