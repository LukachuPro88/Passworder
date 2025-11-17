# Passworder

Passworder is a Python library providing various utilities for password generation, strength checking, input masking, hashing, and verification.

## Features

- Generate random passwords:
  - Letters only (`string_password`)
  - Numbers only (`number_password`)
  - Mixed passwords with letters, numbers, and symbols (`password`)
- Password strength evaluation (`password_strength`)
- Masked password input in the terminal (`password_input`)
- Hash passwords and store in a file (`hash_password`)
- Verify if a password exists in a hashed password file (`find_password`)
- Auto-copy generated passwords to the clipboard

## Installation

```bash
pip install passworder
