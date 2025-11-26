from setuptools import setup, find_packages
import re

def read_version():
    with open("passworder/__init__.py", "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'__version__\s*=\s*["\'](.+)["\']', content)
    if not match:
        raise RuntimeError("Version not found in __init__.py")
    return match.group(1)

setup(
    name="passworder",
    version=read_version(),
    author="Luka Saarivirta",
    description="A lightweight password utilities library.",
    packages=find_packages(),
    install_requires=[
        "pyperclip>=1.8",
        "argon2-cffi>=23.1",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)