import os
import sys
import subprocess

def setup_api_keys():
    print("Meme Culture Time Machine API Key Setup")
    print("======================================")
    
    # Check if GEMINI_API_KEY is already set
    existing_key = os.environ.get("GEMINI_API_KEY")
    if existing_key:
        print(f"GEMINI_API_KEY is already set to: {existing_key[:5]}...")
        change_key = input("Would you like to change it? (y/n): ").strip().lower()
        if change_key != 'y':
            print("Keeping existing API key.")
            return
    
    # Get the Gemini API key
    gemini_key = input("Enter your Gemini API key (get one from https://ai.google.dev/): ").strip()
    
    if not gemini_key:
        print("No API key provided. Exiting.")
        return
    
    # Set for current session
    os.environ["GEMINI_API_KEY"] = gemini_key
    print("GEMINI_API_KEY set for current session.")
    
    # Create a batch/PowerShell script to set it permanently
    if sys.platform == "win32":
        # Create both a batch file and PowerShell script
        with open(os.path.join(os.path.dirname(__file__), "set_api_keys.bat"), "w") as f:
            f.write(f"@echo off\n")
            f.write(f"setx GEMINI_API_KEY \"{gemini_key}\"\n")
            f.write(f"echo API keys set successfully!\n")
            f.write(f"pause\n")
        
        with open(os.path.join(os.path.dirname(__file__), "set_api_keys.ps1"), "w") as f:
            f.write(f"$env:GEMINI_API_KEY = \"{gemini_key}\"\n")
            f.write(f"[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', \"{gemini_key}\", [System.EnvironmentVariableTarget]::User)\n")
            f.write(f"Write-Host \"API keys set successfully!\" -ForegroundColor Green\n")
        
        print("\nTo set API keys permanently:")
        print("Option 1: Run set_api_keys.bat as administrator")
        print("Option 2: Run PowerShell as administrator and execute .\\set_api_keys.ps1")
    else:
        # For Linux/Mac
        shell = os.environ.get("SHELL", "/bin/bash")
        shell_rc = ""
        if "bash" in shell:
            shell_rc = "~/.bashrc"
        elif "zsh" in shell:
            shell_rc = "~/.zshrc"
        
        print(f"\nTo set API keys permanently, add this line to your {shell_rc}:")
        print(f"export GEMINI_API_KEY=\"{gemini_key}\"")
    
    print("\nAfter setting API keys permanently, restart your terminal.")

if __name__ == "__main__":
    setup_api_keys()
