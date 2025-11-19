from setuptools import setup, find_packages

setup(
    name="passworder",
    version="0.0.2",
    author="Luka Saarivirta",
    description="A lightweight password utilities library.",
    packages=find_packages(),
    install_requires=[
        "pyperclip",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",    
        "Operating System :: OS Independent",
    ],
)
