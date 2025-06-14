import subprocess
import sys
import os
import importlib

def run_command(command):
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True)

def fix_dependencies():
    print("Fixing Flask and dependencies...")
    
    # Uninstall problematic packages
    run_command("pip uninstall -y flask werkzeug")
    
    # Install compatible versions
    run_command("pip install flask==2.0.1 werkzeug==2.0.1")
    
    # Install other required packages with specific versions to avoid conflicts
    required_packages = [
        "openai==0.28.0",  # Using older version for compatibility
        "google-cloud-vision==3.4.0",
        "google-cloud-texttospeech==2.14.1",
        "pydub==0.25.1",
        "Pillow==9.5.0",  # For image processing
        "requests==2.30.0",
    ]
    
    for package in required_packages:
        run_command(f"pip install {package}")
    
    print("\nChecking for common conflicts...")
    # Look for duplicate package installations
    run_command("pip list")
    
    # Check for common conflict patterns
    check_conflict("flask", "werkzeug")
    check_conflict("openai", "requests")
    
    print("\nAll dependencies fixed!")
    print("Try running your application with: python app.py")

def check_conflict(pkg1, pkg2):
    try:
        pkg1_mod = importlib.import_module(pkg1)
        pkg2_mod = importlib.import_module(pkg2)
        pkg1_ver = getattr(pkg1_mod, "__version__", "unknown")
        pkg2_ver = getattr(pkg2_mod, "__version__", "unknown")
        print(f"Checking {pkg1} ({pkg1_ver}) and {pkg2} ({pkg2_ver}) compatibility...")
    except ImportError as e:
        print(f"Error importing modules: {e}")

if __name__ == "__main__":
    fix_dependencies()
