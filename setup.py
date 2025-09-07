#!/usr/bin/env python3
"""
Setup script for Kepler-Downloader-DR25
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="kepler-downloader-dr25",
    version="1.0.0",
    author="Kepler-Downloader-DR25 Project",
    description="A comprehensive toolkit for downloading and filtering Kepler DR25 FITS files from NASA's MAST archive",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Kepler-Downloader-DR25",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "kepler-download=get_kepler_dr25:main",
            "kepler-filter=filter_get_kepler_dr25:main",
            "kepler-rebuild-db=util.rebuild_database:main",
            "kepler-check-missing=util.check_missing_kics:main",
            "kepler-stats=util.generate_stats:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "LICENSE"],
    },
)