import os
import sys
import subprocess

required_packages = [
    "asyncio",
    "aiohttp",
    "colorama",
    "pystyle",
    "fade",
    "trio",
    "requests",
]


def install_packages():
    print("Checking for required packages...")
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Package '{package}' is missing. Installing now...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package]
            )


def check_python_version():
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or newer is required.")
        sys.exit(1)
    print(f"Python version {sys.version.split()[0]} is compatible.")


def main():
    print("Starting installation...")
    check_python_version()
    install_packages()
    print("\nSuccess: Installation Finished, You Can Now Use The Bomber.")


if __name__ == "__main__":
    main()
