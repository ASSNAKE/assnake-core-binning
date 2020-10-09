from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
import os, shutil


setup(
    name='assnake-core-binning',
    version='0.0.1',
    packages=find_packages(),
    entry_points = {
        'assnake.plugins': ['assnake-core-binning = assnake_core_binning.snake_module_setup:snake_module']
    }
)