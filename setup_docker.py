import os
import subprocess
import sys
import time

def run_command(command, shell=False):
    """Runs a command and prints output."""
    print(f"Running: {command}")
    try:
        if shell:
            subprocess.check_call(command, shell=True)
        else:
            subprocess.check_call(command.split())
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)

def is_docker_installed():
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_docker():
    print("--- Installing Docker ---")
    print("Note: This requires sudo/root privileges.")

    # Check for sudo/root
    if os.geteuid() != 0:
        print("Error: You must run this script as root (sudo python setup_docker.py) to install Docker.")
        sys.exit(1)

    # Use the convenience script
    try:
        run_command("curl -fsSL https://get.docker.com -o get-docker.sh", shell=True)
        run_command("sh get-docker.sh", shell=True)
        print("Docker installed successfully.")

        # Start Docker service
        run_command("systemctl start docker", shell=True)
        run_command("systemctl enable docker", shell=True)

    except Exception as e:
        print(f"Failed to install Docker: {e}")
        sys.exit(1)

def deploy_container():
    print("\n--- Deploying Application Container ---")

    image_name = "sltv-backend"
    container_name = "sltv-backend-container"

    # 1. Build Image
    print("Building Docker Image (this may take a while)...")
    run_command(f"docker build -t {image_name} .", shell=True)

    # 2. Stop/Remove existing container
    print("Cleaning up old containers...")
    subprocess.run(f"docker stop {container_name}", shell=True, stderr=subprocess.DEVNULL)
    subprocess.run(f"docker rm {container_name}", shell=True, stderr=subprocess.DEVNULL)

    # 3. Run Container
    print("Starting new container...")
    # We mount the .env file and expose port 8000
    # We also add --shm-size=2g to prevent Chrome crashes in Docker
    cmd = (
        f"docker run -d "
        f"--name {container_name} "
        f"-p 8000:8000 "
        f"--env-file .env "
        f"--shm-size=2g "
        f"--restart unless-stopped "
        f"{image_name}"
    )
    run_command(cmd, shell=True)

    print("\n--- Deployment Complete ---")
    print(f"Container '{container_name}' is running on port 8000.")
    print("Check logs with: docker logs -f sltv-backend-container")

def main():
    print("--- Docker Deployment Script ---")

    if not is_docker_installed():
        print("Docker is NOT installed.")
        install_docker()
    else:
        print("Docker is already installed.")

    deploy_container()

if __name__ == "__main__":
    main()
