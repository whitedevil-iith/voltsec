"""
Setup script for voltsec_ai.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README_AI.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="voltsec-ai",
    version="0.1.0",
    author="VoltSec Team",
    description="Python-based multi-agent system for code vulnerability and performance analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/whitedevil-iith/voltsec",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "crewai>=0.28.0",
        "langchain>=0.1.0",
        "langchain-community>=0.0.20",
        "chromadb>=0.4.22",
        "pypdf>=3.17.0",
        "python-docx>=1.1.0",
        "python-dotenv>=1.0.0",
        "typing-extensions>=4.9.0",
    ],
    entry_points={
        "console_scripts": [
            "voltsec-ai=voltsec_ai.main:main",
        ],
    },
    include_package_data=True,
    keywords="security vulnerability performance analysis ai multi-agent crewai langchain ollama",
)
