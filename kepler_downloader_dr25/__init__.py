"""
Kepler-Downloader-DR25
A comprehensive toolkit for downloading and filtering Kepler DR25 FITS files from NASA's MAST archive.
"""

__version__ = "1.1.0"
__author__ = "akira921x"
__email__ = "cl756@gwmail.gwu.edu"

from .downloader import main as download_main
from .filter import main as filter_main

__all__ = ["download_main", "filter_main"]