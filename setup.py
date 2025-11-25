from setuptools import setup, find_packages
from passworder import __version__

setup(
    name="passworder",
    version=__version__,
    author="Luka Saarivirta",
    description="A lightweight password utilities library.",
    packages=find_packages(),
    install_requires=[
        "pyperclip",
        "argon2-cffi",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)