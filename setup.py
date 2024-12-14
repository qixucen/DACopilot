# setup.py
from setuptools import setup, find_packages

setup(
    name="multi-agent-analysis",
    version="0.1.0",
    description="A multi-agent system for automated data analysis",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0", 
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "pytest>=6.2.0"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "run-analysis=main:main",
        ],
    },
    package_data={
        "tests": ["data/*.csv"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)