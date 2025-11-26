import sys
import os
import subprocess
import importlib.util
from IPython import get_ipython

def init():
    # 1. Install dependencies if missing (Silent)
    required_packages = ['pandas', 'openpyxl', 'ipython']
    missing = []
    for pkg in required_packages:
        if importlib.util.find_spec(pkg) is None:
            missing.append(pkg)
    
    if missing:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install"] + missing,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            pass 

    # 2. Setup Paths
    current_dir = os.getcwd()
    scripts_path = os.path.join(current_dir, 'scripts')
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)
    
    # 3. Load Magic
    try:
        ip = get_ipython()
        if ip is None:
            return

        # Use run_line_magic instead of magic to avoid deprecation warning
        # We reload if it's already there, or load it if not.
        # Using %reload_ext is safer than importlib for magics as it handles the lifecycle
        ip.run_line_magic('reload_ext', 'simulator_magic')
        
        # Success - explicit silence requested by user
        
    except Exception:
        # Fail silently or minimal error if critical
        pass

if __name__ == "__main__":
    init()
