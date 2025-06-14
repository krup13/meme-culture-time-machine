import os
import requests
import zipfile
import shutil
import subprocess
import sys

def setup_ffmpeg():
    print("Setting up ffmpeg...")
    
    # Create directories if they don't exist
    tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")
    ffmpeg_dir = os.path.join(tools_dir, "ffmpeg")
    
    if not os.path.exists(tools_dir):
        os.makedirs(tools_dir)
        
    if not os.path.exists(ffmpeg_dir):
        os.makedirs(ffmpeg_dir)
    
    # Download ffmpeg
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(tools_dir, "ffmpeg.zip")
    
    print("Downloading ffmpeg (this might take a few minutes)...")
    r = requests.get(ffmpeg_url, stream=True)
    with open(zip_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    
    # Extract the zip file
    print("Extracting ffmpeg...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(tools_dir)
    
    # Find the extracted directory (it has a version number in it)
    extract_dir = None
    for item in os.listdir(tools_dir):
        if item.startswith("ffmpeg-") and os.path.isdir(os.path.join(tools_dir, item)):
            extract_dir = os.path.join(tools_dir, item)
            break
    
    if not extract_dir:
        print("Error: Couldn't find extracted ffmpeg directory")
        return
    
    # Move bin contents to our ffmpeg directory
    bin_dir = os.path.join(extract_dir, "bin")
    for item in os.listdir(bin_dir):
        shutil.copy2(os.path.join(bin_dir, item), ffmpeg_dir)
    
    # Add to PATH for the current session
    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]
    
    # Clean up
    os.remove(zip_path)
    shutil.rmtree(extract_dir)
    
    print(f"ffmpeg installed to {ffmpeg_dir}")
    print("Added to PATH for current session")
    print("\nTo make this permanent, add this directory to your system PATH:")
    print(ffmpeg_dir)
    
    # Test if it worked
    try:
        subprocess.run(["ffmpeg", "-version"], check=True)
        print("\nffmpeg installation verified!")
    except:
        print("\nWarning: ffmpeg was installed but not found in PATH.")
        print("You may need to restart your terminal or add it to PATH manually.")

if __name__ == "__main__":
    setup_ffmpeg()
