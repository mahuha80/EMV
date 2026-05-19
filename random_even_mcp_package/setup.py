from setuptools import setup, find_packages

setup(
    name="random-even-mcp",
    version="1.0.0",
    author="AI Assistant",
    description="MCP Server for RandomEvenLibrary - Generate random even numbers from 1 to 20",
    long_description="Model Context Protocol server for generating random even numbers",
    url="https://github.com/yourusername/random-even-mcp",
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
            "random-even-mcp=random_even_mcp.random_even_mcp:main",
        ],
    },
)

