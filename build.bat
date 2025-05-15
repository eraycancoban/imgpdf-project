@echo off
REM This batch file builds the imgpdf application executable using PyInstaller.

REM Create resources directory if it doesn't exist
if not exist "src\resources" mkdir src\resources

REM Navigate to the src directory
cd src

REM Use PyInstaller with additional options for better compatibility
pyinstaller --onefile --windowed --icon=resources/icon.ico ^
    --add-data "resources;resources" ^
    --name "ImagePDFMerger" ^
    --noconsole ^
    imgpdf.py

REM Move the generated executable to the project root
move dist\ImagePDFMerger.exe ..\

REM Clean up the build files
rmdir /s /q build
rmdir /s /q dist
del ImagePDFMerger.spec

echo Build complete! The executable is located in the project root directory.
echo Press any key to exit...
pause >nul