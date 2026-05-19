from setuptools import setup, find_packages
import os

# Read README if it exists
long_description = "Robot Framework library for generating random even numbers from 1 to 20"
if os.path.exists("README.md"):
    with open("README.md") as f:
        long_description = f.read()

setup(
    name="RandomEvenLibrary",
    version="1.0.0",
    author="AI Assistant",
    description="Robot Framework library for generating random even numbers from 1 to 20",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/RandomEvenLibrary",
    py_modules=["RandomEvenLibrary"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Framework :: Robot Framework",
    ],
    python_requires=">=3.6",
)

