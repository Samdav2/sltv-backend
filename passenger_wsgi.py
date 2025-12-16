import os
import sys

# Insert project directory to sys.path so that packages can be imported
sys.path.insert(0, os.path.dirname(__file__))

# --- LOCAL LIBRARY INJECTION ---
# Add local_libs/usr/lib64 to LD_LIBRARY_PATH for Chrome dependencies
base_dir = os.path.dirname(os.path.abspath(__file__))
local_lib_path = os.path.join(base_dir, "local_libs", "usr", "lib64")

if os.path.exists(local_lib_path):
    current_ld_path = os.environ.get("LD_LIBRARY_PATH", "")
    if local_lib_path not in current_ld_path:
        os.environ["LD_LIBRARY_PATH"] = f"{local_lib_path}:{current_ld_path}"
        # Also re-exec if needed, but for shared libs usually setting env before import helps
        # However, for subprocesses (like Chrome), os.environ is enough.
# -------------------------------

# Import the FastAPI app
# 'app.main' refers to app/main.py
# 'app' is the FastAPI instance variable in main.py
from app.main import app as application
