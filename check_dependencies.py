import os
import subprocess
import sys

def check_dependencies():
    print("--- Chrome Dependency Checker ---")

    # 1. Find Chrome Binary
    # Try to read from .env first, or guess the location
    chrome_path = None

    # Try to find in local bin folder first (default from install_chrome.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_bin = os.path.join(base_dir, "bin", "chrome-linux64", "chrome")

    if os.path.exists(local_bin):
        chrome_path = local_bin
    else:
        # Check .env
        env_path = os.path.join(base_dir, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    if line.startswith("CHROME_BINARY_PATH="):
                        chrome_path = line.split("=", 1)[1].strip()
                        break

    if not chrome_path or not os.path.exists(chrome_path):
        print(f"Error: Could not find Chrome binary at: {chrome_path}")
        print("Please run 'python install_chrome.py' first.")
        return

    print(f"Checking dependencies for: {chrome_path}")

    # 2. Run ldd
    try:
        result = subprocess.run(["ldd", chrome_path], capture_output=True, text=True)
        output = result.stdout

        missing = []
        for line in output.splitlines():
            if "not found" in line:
                missing.append(line.strip())

        if missing:
            print("\n[CRITICAL] Missing System Libraries:")
            for lib in missing:
                print(f"  - {lib}")
            print("\nSOLUTION: You need to ask your hosting provider to install these packages.")
            print("Common missing packages on CentOS/cPanel:")
            print("  sudo yum install nss atk java-atk-wrapper at-spi2-atk gtk3 libXcomposite libXrandr alsa-lib pango at-spi2-core cups-libs")
        else:
            print("\n[SUCCESS] All system dependencies seem to be present!")

    except Exception as e:
        print(f"Error running ldd: {e}")

if __name__ == "__main__":
    check_dependencies()
