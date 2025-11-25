import re

file_path = "passworder/__init__.py"

with open(file_path, "r") as f:
    content = f.read()

# Find __version__ = "1.0.3"
match = re.search(r'__version__ = ["\'](\d+)\.(\d+)\.(\d+)["\']', content)
if match:
    major, minor, patch = map(int, match.groups())
    patch += 1  # bump patch version
    new_version = f'{major}.{minor}.{patch}'
    content = re.sub(
        r'__version__ = ["\'](\d+)\.(\d+)\.(\d+)["\']',
        f'__version__ = "{new_version}"',
        content
    )

    with open(file_path, "w") as f:
        f.write(content)


