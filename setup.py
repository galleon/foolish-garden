import os.path
import sys

from setuptools import find_packages, setup

from version import VERSION

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="foolish-garden",
    version=VERSION,
    author="Guillaume Alleon",
    author_email="guillaume.alleon@gmail.com",
    zip_safe=False,
    description="A package containing few 2d GYM enviromenments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/galleon/foolish-garden",
    project_urls={
        "Bug Tracker": "https://github.com/galleon/foolish-garden/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["gym>=0.15.7", "numpy>=1.18.1", "stable_baselines3>=1.3.0"],
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.7",
)
