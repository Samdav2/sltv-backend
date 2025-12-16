import os
import sys
import json
import shutil
import urllib.request
import zipfile
import stat

def install_chrome():
    print("--- Chrome & ChromeDriver Installer for Linux ---")

    # 1. Define Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(base_dir, "bin")

    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
        print(f"Created bin directory: {bin_dir}")

    # 2. Fetch Latest Stable Version Info
    print("Fetching latest stable version info...")
    json_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

    try:
        with urllib.request.urlopen(json_url) as response:
            data = json.loads(response.read().decode())

        stable_channel = data["channels"]["Stable"]
        version = stable_channel["version"]
        print(f"Latest Stable Version: {version}")

        downloads = stable_channel["downloads"]
        chrome_url = None
        driver_url = None

        for item in downloads["chrome"]:
            if item["platform"] == "linux64":
                chrome_url = item["url"]
                break

        for item in downloads["chromedriver"]:
            if item["platform"] == "linux64":
                driver_url = item["url"]
                break

        if not chrome_url or not driver_url:
            print("Error: Could not find download URLs for linux64.")
            return

    except Exception as e:
        print(f"Error fetching version info: {e}")
        return

    # 3. Download Files
    def download_file(url, dest_path):
        print(f"Downloading {url}...")
        try:
            with urllib.request.urlopen(url) as response, open(dest_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            print("Download complete.")
        except Exception as e:
            print(f"Download failed: {e}")
            sys.exit(1)

    chrome_zip = os.path.join(bin_dir, "chrome-linux64.zip")
    driver_zip = os.path.join(bin_dir, "chromedriver-linux64.zip")

    download_file(chrome_url, chrome_zip)
    download_file(driver_url, driver_zip)

    # 4. Extract Files
    print("Extracting files...")

    def extract_zip(zip_path, extract_to):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

    extract_zip(chrome_zip, bin_dir)
    extract_zip(driver_zip, bin_dir)

    # 5. Cleanup & Permissions
    print("Cleaning up and setting permissions...")
    os.remove(chrome_zip)
    os.remove(driver_zip)

    chrome_binary = os.path.join(bin_dir, "chrome-linux64", "chrome")
    driver_binary = os.path.join(bin_dir, "chromedriver-linux64", "chromedriver")

    # Make executable
    st = os.stat(chrome_binary)
    os.chmod(chrome_binary, st.st_mode | stat.S_IEXEC)

    st = os.stat(driver_binary)
    os.chmod(driver_binary, st.st_mode | stat.S_IEXEC)

    # 6. Output Instructions
    print("\n--- Installation Complete ---")
    print(f"Chrome Binary: {chrome_binary}")
    print(f"ChromeDriver: {driver_binary}")
    print("\nIMPORTANT: Add the following to your .env file:")
    print("-" * 50)
    print(f"CHROME_BINARY_PATH={chrome_binary}")
    print(f"CHROMEDRIVER_PATH={driver_binary}")
    print("-" * 50)

if __name__ == "__main__":
    install_chrome()
