from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pydiagrams",
    version="0.1.0",
    author="PyDiagrams Team",
    author_email="info@pydiagrams.org",
    description="A comprehensive Python library for generating various types of diagrams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pydiagrams/pydiagrams",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pillow>=8.0.0",
        "pydot>=1.4.2",
        "svgwrite>=1.4.0",
        "reportlab>=3.6.0",
        "typing-extensions>=4.0.0",
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.5b2",
            "isort>=5.9.0",
            "mypy>=0.900",
            "flake8>=3.9.0",
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pydiagrams=pydiagrams.cli:main",
        ],
    },
) 