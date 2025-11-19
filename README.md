# Passworder

Passworder is a Python library providing utilities for password generation, strength checking, masked password input, hashing, and password verification.

## ✨ Features

- Generate random passwords
  - Uppercase/lowercase/symbol combinations (`string_password`)
  - Numbers only (`number_password`)
  - Fully customizable strong passwords (`password`)
- Password strength evaluation (`password_strength`)
- Terminal masked password input (`password_input`)
- Hash passwords and save them to a file (`hash_password`)
- Check if a password exists in a hashed file (`find_password`)
- Auto-copy passwords to clipboard via `pyperclip`

---

## 📦 Installation

Once published to PyPI, install with:

```bash
pip install passworder  