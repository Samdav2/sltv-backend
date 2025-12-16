import os
import subprocess
import sys

def diagnose_chromedriver():
    print("--- ChromeDriver Diagnostic Tool ---")

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Find ChromeDriver
    chromedriver_path = os.path.join(base_dir, "bin", "chromedriver-linux64", "chromedriver")

    if not os.path.exists(chromedriver_path):
        print(f"ChromeDriver not found at: {chromedriver_path}")
        # Try to find it
        for root, dirs, files in os.walk(base_dir):
            if 'chromedriver' in files:
                chromedriver_path = os.path.join(root, 'chromedriver')
                print(f"Found ChromeDriver at: {chromedriver_path}")
                break

    if not os.path.exists(chromedriver_path):
        print("ERROR: ChromeDriver not found anywhere!")
        return

    print(f"ChromeDriver: {chromedriver_path}")

    # 1. Check file permissions
    print("\n[1] Checking file permissions...")
    stat = os.stat(chromedriver_path)
    print(f"  Mode: {oct(stat.st_mode)}")
    is_executable = os.access(chromedriver_path, os.X_OK)
    print(f"  Executable: {is_executable}")

    if not is_executable:
        print("  Fixing permissions...")
        os.chmod(chromedriver_path, 0o755)

    # 2. Check library dependencies
    print("\n[2] Checking library dependencies...")
    try:
        result = subprocess.run(
            ["ldd", chromedriver_path],
            capture_output=True,
            text=True
        )

        missing = []
        for line in result.stdout.splitlines():
            if "not found" in line:
                missing.append(line.strip())

        if missing:
            print("  MISSING libraries:")
            for lib in missing:
                print(f"    {lib}")
        else:
            print("  All libraries OK")

    except Exception as e:
        print(f"  Error running ldd: {e}")

    # 3. Try to run ChromeDriver directly
    print("\n[3] Running ChromeDriver directly...")

    # Set LD_LIBRARY_PATH
    local_libs = os.path.join(base_dir, "local_libs", "usr", "lib", "x86_64-linux-gnu")
    env = os.environ.copy()
    if os.path.exists(local_libs):
        env["LD_LIBRARY_PATH"] = f"{local_libs}:{env.get('LD_LIBRARY_PATH', '')}"
        print(f"  Set LD_LIBRARY_PATH: {local_libs}")

    try:
        result = subprocess.run(
            [chromedriver_path, "--version"],
            capture_output=True,
            text=True,
            env=env,
            timeout=10
        )
        print(f"  Exit code: {result.returncode}")
        print(f"  Stdout: {result.stdout.strip()}")
        if result.stderr:
            print(f"  Stderr: {result.stderr.strip()}")

    except subprocess.TimeoutExpired:
        print("  ChromeDriver timed out")
    except Exception as e:
        print(f"  Error: {e}")

    # 4. Check Chrome binary
    print("\n[4] Checking Chrome binary...")
    chrome_path = os.path.join(base_dir, "bin", "chrome-linux64", "chrome")

    if os.path.exists(chrome_path):
        print(f"  Chrome: {chrome_path}")

        # Check if executable
        is_executable = os.access(chrome_path, os.X_OK)
        print(f"  Executable: {is_executable}")

        # Try to get version
        try:
            result = subprocess.run(
                [chrome_path, "--version"],
                capture_output=True,
                text=True,
                env=env,
                timeout=10
            )
            print(f"  Version: {result.stdout.strip()}")
            if result.stderr:
                print(f"  Stderr: {result.stderr.strip()}")
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print(f"  Chrome not found at: {chrome_path}")

if __name__ == "__main__":
    diagnose_chromedriver()
