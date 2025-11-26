import re

file_path = "passworder/__init__.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r'^__version__\s*=\s*["\'](\d+)\.(\d+)\.(\d+)["\']', content, re.MULTILINE)
if match:
    major, minor, patch = map(int, match.groups())
    patch += 1  # bump patch version
    new_version = f"{major}.{minor}.{patch}"

    content = re.sub(
        r'^__version__\s*=\s*["\'](\d+)\.(\d+)\.(\d+)["\']',
        f'__version__ = "{new_version}"',
        content,
        flags=re.MULTILINE
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Version bumped to {new_version}")
else:
    print("No __version__ found in __init__.py")