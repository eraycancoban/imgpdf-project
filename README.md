# imgpdf Project

## Overview
The imgpdf project is a Python application that allows users to convert images into PDF files. It features a user-friendly graphical interface built with Tkinter, image processing capabilities using the Pillow library, and PDF generation with ReportLab.

## Project Structure
```
imgpdf-project
├── src
│   ├── imgpdf.py          # Main application code for converting images to PDF
│   └── resources
│       └── icon.ico       # Icon resource for the application window
├── requirements.txt       # Lists dependencies required for the project
├── setup.py               # Packaging script for the application
├── build.bat              # Batch script for building the executable on Windows
├── build.sh               # Shell script for building the executable on Unix-based systems
└── README.md              # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd imgpdf-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/imgpdf.py
```

## Building the Executable

### Windows
To build the executable on Windows, run the `build.bat` script:
```
build.bat
```

### Unix-based Systems
To build the executable on Unix-based systems, run the `build.sh` script:
```
bash build.sh
```

## Dependencies
The project requires the following Python libraries:
- Tkinter
- Pillow (PIL)
- ReportLab

These libraries are listed in the `requirements.txt` file.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.