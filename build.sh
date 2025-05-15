#!/bin/bash

# This script builds the imgpdf application into an executable using PyInstaller.

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null
then
    echo "PyInstaller could not be found. Please install it using 'pip install pyinstaller'."
    exit
fi

# Create a build directory if it doesn't exist
BUILD_DIR="build"
if [ ! -d "$BUILD_DIR" ]; then
    mkdir "$BUILD_DIR"
fi

# Navigate to the src directory
cd src

# Build the executable
pyinstaller --onefile --windowed --icon=resources/icon.ico imgpdf.py

# Move the executable to the build directory
mv dist/imgpdf ../$BUILD_DIR/

# Clean up unnecessary files
rm -rf build/ dist/ imgpdf.spec

echo "Build completed. The executable is located in the '$BUILD_DIR' directory."