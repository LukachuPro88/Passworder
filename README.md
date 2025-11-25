# Passworder

Passworder is a Python library for secure password generation, strength checking, masked input, hashing, and verification.

## ✨ Features

- **Random Passwords**
  - `string_password`: letters, numbers, symbols
  - `number_password`: numbers only
  - `password`: fully customizable strong passwords
  - `pronounceable_password`: easy-to-remember passwords
  - `custom_password`: use your own character set
- **Password Utilities**
  - `password_strength`: evaluate password strength
  - `password_input`: terminal input with hidden characters
  - `hash_password`: hash and save passwords to a file
  - `find_password`: verify password presence in a file
  - `brute_force_protection`: protect against multiple incorrect attempts
  - Clipboard auto-copy support via `pyperclip`

## 📦 Installation

Install from PyPI:

```bash
pip install passworder