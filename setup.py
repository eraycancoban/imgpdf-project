from setuptools import setup, find_packages

setup(
    name="imgpdf-project",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A GUI application for converting images to PDF.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/imgpdf-project",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        "Pillow",
        "reportlab",
        "tkinter"
    ],
    entry_points={
        'console_scripts': [
            'imgpdf=imgpdf:main',  # Assuming you have a main function in imgpdf.py
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)