#!/usr/bin/env python3
"""
Setup script for the Exoplanet Classifier
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Execute a command and display the result."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if the Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected!")
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up Exoplanet Classifier...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if pip is available
    if not run_command("pip --version", "Checking pip"):
        print("❌ pip not found. Install pip first.")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies.")
        sys.exit(1)
    
    # Check if model exists
    if not os.path.exists("data/model_and_features.pkl"):
        print("⚠️  Model not found in data/model_and_features.pkl")
        print("   Make sure the model file is present.")
    
    # Check if example file exists
    if not os.path.exists("example_exoplanet_spreadsheet.csv"):
        print("⚠️  Example file not found")
        print("   Make sure example_exoplanet_spreadsheet.csv is present.")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: streamlit run app.py")
    print("2. Open http://localhost:8501 in your browser")
    print("3. Start classifying exoplanets!")
    print("\n📚 Documentation:")
    print("- README.md: Complete guide")
    print("- DEPLOY.md: Deployment instructions")
    print("- CONTRIBUTING.md: How to contribute")
    print("\n🌟 Have fun exploring the universe!")

if __name__ == "__main__":
    main()
