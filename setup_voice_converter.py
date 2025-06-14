import subprocess
import sys
import os
import platform

def install_package(package):
    print(f"Installing {package}...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")
        return False
    return True

def setup_voice_dependencies():
    print("Setting up Voice Era Converter dependencies...")
    
    # List of required packages
    packages = [
        'SpeechRecognition==3.10.0',
        'google-cloud-speech==2.22.0',
        'google-cloud-texttospeech==2.14.1',
        'pydub==0.25.1',
        'pyaudio==0.2.13',  # For microphone recording
        'requests==2.30.0'
    ]
    
    # Install PyAudio with special handling for Windows
    if platform.system() == 'Windows':
        try:
            import pyaudio
            print("PyAudio is already installed.")
        except ImportError:
            print("Installing PyAudio (Windows)...")
            print("Attempting to install PyAudio using pip...")
            success = install_package('pyaudio')
            
            if not success:
                print("\nPyAudio installation failed. Try this alternative approach:")
                print("1. Run: pip install pipwin")
                print("2. Then: pipwin install pyaudio")
                
                # Try the pipwin approach automatically
                print("Attempting pipwin installation...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'pipwin'], check=False)
                subprocess.run([sys.executable, '-m', 'pipwin', 'install', 'pyaudio'], check=False)
    
    # Install other packages
    for package in packages:
        if 'pyaudio' not in package.lower():  # Skip PyAudio as we handled it separately
            install_package(package)
    
    # Check if ffmpeg is installed
    print("\nChecking for ffmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("ffmpeg is installed and accessible.")
    except FileNotFoundError:
        print("ffmpeg is not found. Please run setup_ffmpeg.py first.")
    
    # Check Google Cloud credentials
    print("\nChecking Google Cloud credentials...")
    credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if credentials_path:
        if os.path.exists(credentials_path):
            print(f"Google Cloud credentials found at: {credentials_path}")
        else:
            print(f"Google Cloud credentials path set but file not found: {credentials_path}")
    else:
        print("Google Cloud credentials not set. Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
        print("For more information, visit: https://cloud.google.com/docs/authentication/getting-started")
    
    print("\nSetup completed. If you encountered errors, please address them manually.")
    print("For the voice converter to work properly, you need:")
    print("1. ffmpeg installed and in your PATH")
    print("2. PyAudio correctly installed")
    print("3. Google Cloud credentials set up for Speech and Text-to-Speech APIs")

if __name__ == "__main__":
    setup_voice_dependencies()
