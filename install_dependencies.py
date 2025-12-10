import subprocess
import sys
import os

def install_packages():
    """
    Installs packages listed in requirements.txt using pip.
    """
    requirements_file = "requirements.txt"

    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found in the current directory.")
        sys.exit(1)

    print("Starting dependency installation...")

    try:
        # 1. Upgrade pip to ensure we have the latest version
        print("Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

        # 2. Install wheel to help with building packages
        print("Installing wheel...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "wheel"])

        # 3. Install requirements
        print(f"Installing packages from {requirements_file}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])

        print("\nSUCCESS: All dependencies installed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Failed to install dependencies. Command failed with exit code {e.returncode}.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_packages()
