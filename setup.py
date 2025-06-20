import sys
import subprocess
import os

REQUIREMENTS = [
    "numpy==1.26.4",
    "matplotlib==3.8.4",
    "scipy==1.13.0",
    "pandas==2.2.1"
]

def is_installed(package):
    try:
        __import__(package.split('==')[0])
        return True
    except ImportError:
        return False

def install_packages():
    print("Setting up fracture analysis environment...")
    python_exec = sys.executable
    
    # Install with no cache to prevent conflicts
    subprocess.check_call([
        python_exec, "-m", "pip", "install", 
        "--no-cache-dir", "--force-reinstall"
    ] + REQUIREMENTS, stdout=subprocess.DEVNULL)
    
    print("✓ Environment ready")

def verify_matplotlib():
    try:
        import matplotlib as mpl
        print(f"Matplotlib {mpl.__version__} installed at:")
        print(mpl.__file__)
        return True
    except Exception as e:
        print(f"Matplotlib verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Skip setup in cloud environments
    if "COLAB_JUPYTER_IP" in os.environ or "KAGGLE_KERNEL_RUN_TYPE" in os.environ:
        print("Cloud environment detected - skipping setup")
    else:
        if not all(is_installed(pkg) for pkg in REQUIREMENTS) or not verify_matplotlib():
            install_packages()
            verify_matplotlib()
