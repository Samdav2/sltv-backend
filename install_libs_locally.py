import os
import urllib.request
import shutil
import tarfile
import lzma
import gzip

# Ubuntu 20.04 (Focal) packages - use xz compression, not zstd
DEB_URLS = [
    # at-spi2 packages
    "http://archive.ubuntu.com/ubuntu/pool/main/a/at-spi2-atk/libatk-bridge2.0-0_2.34.2-0ubuntu2~20.04.1_amd64.deb",
    "http://archive.ubuntu.com/ubuntu/pool/main/a/at-spi2-core/libatspi2.0-0_2.36.0-2_amd64.deb",
    # mesa/gbm
    "http://archive.ubuntu.com/ubuntu/pool/main/m/mesa/libgbm1_21.2.6-0ubuntu0.1~20.04.2_amd64.deb",
    # alsa
    "http://archive.ubuntu.com/ubuntu/pool/main/a/alsa-lib/libasound2_1.2.2-2.1ubuntu2.5_amd64.deb",
    # X11 libs
    "http://archive.ubuntu.com/ubuntu/pool/main/libx/libxcomposite/libxcomposite1_0.4.5-1_amd64.deb",
    "http://archive.ubuntu.com/ubuntu/pool/main/libx/libxrandr/libxrandr2_1.5.2-0ubuntu1_amd64.deb",
    "http://archive.ubuntu.com/ubuntu/pool/main/libx/libxkbcommon/libxkbcommon0_0.10.0-1_amd64.deb",
    "http://archive.ubuntu.com/ubuntu/pool/main/libx/libxdamage/libxdamage1_1.1.5-2_amd64.deb",
    # NSS/NSPR
    "http://security.ubuntu.com/ubuntu/pool/main/n/nss/libnss3_3.49.1-1ubuntu1.9_amd64.deb",
    "http://archive.ubuntu.com/ubuntu/pool/main/n/nspr/libnspr4_4.25-1_amd64.deb",
    # Additional deps
    "http://archive.ubuntu.com/ubuntu/pool/main/a/atk1.0/libatk1.0-0_2.35.1-1ubuntu2_amd64.deb",
    "http://security.ubuntu.com/ubuntu/pool/main/c/cups/libcups2_2.3.1-9ubuntu1.6_amd64.deb",
    "http://archive.ubuntu.com/ubuntu/pool/main/libx/libxfixes/libxfixes3_5.0.3-2_amd64.deb",
]

def extract_ar(ar_path, output_dir):
    """Pure Python AR archive extractor."""
    with open(ar_path, 'rb') as f:
        magic = f.read(8)
        if magic != b'!<arch>\n':
            raise ValueError("Not a valid AR archive")

        while True:
            header = f.read(60)
            if len(header) < 60:
                break

            name = header[0:16].decode('ascii').strip().rstrip('/')
            size = int(header[48:58].decode('ascii').strip())

            if name == 'debian-binary' or name.startswith('control'):
                f.read(size)
                if size % 2 == 1:
                    f.read(1)
                continue

            if name.startswith('data.tar'):
                data = f.read(size)
                data_path = os.path.join(output_dir, name)
                with open(data_path, 'wb') as out:
                    out.write(data)
                return data_path

            f.read(size)
            if size % 2 == 1:
                f.read(1)

    return None

def extract_tar(tar_path, output_dir):
    """Extract tar.xz, tar.gz, or plain tar using Python only."""
    try:
        if tar_path.endswith('.xz'):
            with lzma.open(tar_path) as xz:
                with tarfile.open(fileobj=xz) as tar:
                    tar.extractall(output_dir)
            return True
        elif tar_path.endswith('.gz'):
            with gzip.open(tar_path, 'rb') as gz:
                with tarfile.open(fileobj=gz) as tar:
                    tar.extractall(output_dir)
            return True
        elif tar_path.endswith('.zst'):
            # Try pure Python zstd if available
            try:
                import zstandard as zstd
                with open(tar_path, 'rb') as zst_file:
                    dctx = zstd.ZstdDecompressor()
                    with dctx.stream_reader(zst_file) as reader:
                        with tarfile.open(fileobj=reader) as tar:
                            tar.extractall(output_dir)
                return True
            except ImportError:
                print("(zstandard module not available)")
                return False
        else:
            with tarfile.open(tar_path) as tar:
                tar.extractall(output_dir)
            return True
    except Exception as e:
        print(f"(Error: {e})")
        return False

def install_libs():
    print("--- Local Library Installer v4 (Ubuntu 20.04/xz) ---")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    libs_dir = os.path.join(base_dir, "local_libs")
    temp_dir = os.path.join(base_dir, "temp_debs")

    # Clean up
    if os.path.exists(libs_dir):
        shutil.rmtree(libs_dir)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    os.makedirs(libs_dir)
    os.makedirs(temp_dir)

    print(f"Target: {libs_dir}")

    success_count = 0
    for i, url in enumerate(DEB_URLS):
        filename = url.split("/")[-1]
        deb_path = os.path.join(temp_dir, filename)

        print(f"\n[{i+1}/{len(DEB_URLS)}] {filename}")

        # Download
        try:
            print("  Downloading...", end=" ")
            urllib.request.urlretrieve(url, deb_path)
            print("OK")
        except Exception as e:
            print(f"FAILED - {e}")
            continue

        # Extract DEB (AR archive)
        try:
            print("  Extracting AR...", end=" ")
            data_tar = extract_ar(deb_path, temp_dir)
            if not data_tar:
                print("FAILED - No data.tar found")
                continue
            print("OK")
        except Exception as e:
            print(f"FAILED - {e}")
            continue

        # Extract TAR
        try:
            print("  Extracting TAR...", end=" ")
            if extract_tar(data_tar, libs_dir):
                print("OK")
                success_count += 1
            else:
                print("FAILED")
        except Exception as e:
            print(f"FAILED - {e}")

        # Clean up data.tar
        if os.path.exists(data_tar):
            os.remove(data_tar)

    # Cleanup
    shutil.rmtree(temp_dir)

    # Summary
    print(f"\n--- Extraction Complete: {success_count}/{len(DEB_URLS)} packages ---")

    # Find lib paths
    lib_paths = []
    for root, dirs, files in os.walk(libs_dir):
        if any(f.endswith(".so") or ".so." in f for f in files):
            lib_paths.append(root)

    if lib_paths:
        combined = ":".join(lib_paths)
        print(f"\n✓ Libraries found in:")
        for p in lib_paths:
            print(f"  {p}")
        print(f"\nLD_LIBRARY_PATH={combined}")

        with open(os.path.join(base_dir, "local_libs_env.sh"), "w") as f:
            f.write(f"export LD_LIBRARY_PATH={combined}:$LD_LIBRARY_PATH\n")
    else:
        print("\n✗ No libraries found!")

if __name__ == "__main__":
    install_libs()
