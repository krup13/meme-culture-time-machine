import subprocess

def install_dependencies():
    print("Installing required packages...")
    packages = [
        "flask",
        "google-generativeai",  # For Gemini API
        "google-cloud-vision",
        "google-cloud-texttospeech",
        "pydub"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.run(["pip", "install", package], check=True)
    
    print("All dependencies installed successfully!")

if __name__ == "__main__":
    install_dependencies()
