from setuptools import setup, find_packages

setup(
    name="random-odd-mcp",
    version="1.0.0",
    author="AI Assistant",
    description="MCP Server for RandomOddLibrary - Generate random odd numbers from 1 to 20",
    long_description="Model Context Protocol server for generating random odd numbers",
    url="https://github.com/yourusername/random-odd-mcp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "random-odd-mcp=random_odd_mcp.random_odd_mcp:main",
        ],
    },
)

