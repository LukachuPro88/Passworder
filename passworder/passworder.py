import random as rnd
import string
import pyperclip
import sys
import tty
import termios
import hashlib

strong_chars = string.punctuation

class Random:
    @staticmethod
    def string_password(length, uppercase=True, lowercase=True, symbols=True, copy=True):
        chars = ""
        if uppercase:
            chars += string.ascii_uppercase
        if lowercase:
            chars += string.ascii_lowercase
        if symbols:
            chars += string.punctuation
        if not chars:
            chars = string.ascii_letters

        password_chars = []

        if uppercase:
            password_chars.append(rnd.choice(string.ascii_uppercase))
        if lowercase:
            password_chars.append(rnd.choice(string.ascii_lowercase))
        if symbols:
            password_chars.append(rnd.choice(string.punctuation))

        remaining_length = length - len(password_chars)
        for _ in range(remaining_length):
            password_chars.append(rnd.choice(chars))

        rnd.shuffle(password_chars)
        password_str = "".join(password_chars)

        if copy:
            try:
                pyperclip.copy(password_str)
                print("Copied!")
            except pyperclip.PyperclipException:
                print("Error copying password!")

        return password_str

    @staticmethod
    def number_password(length, copy=True):
        password_chars = [str(rnd.randint(0, 9)) for _ in range(length)]
        password_str = "".join(password_chars)

        if copy:
            try:
                pyperclip.copy(password_str)
                print("Copied!")
            except pyperclip.PyperclipException:
                print("Error copying password!")

        return password_str

    @staticmethod
    def password(length, uppercase=True, lowercase=True, symbols=True, digits=True, copy=True):
        chars = ""
        if uppercase:
            chars += string.ascii_uppercase
        if lowercase:
            chars += string.ascii_lowercase
        if symbols:
            chars += string.punctuation
        if digits:
            chars += string.digits
        if not chars:
            chars = string.ascii_letters

        password_chars = []

        if uppercase:
            password_chars.append(rnd.choice(string.ascii_uppercase))
        if lowercase:
            password_chars.append(rnd.choice(string.ascii_lowercase))
        if digits:
            password_chars.append(rnd.choice(string.digits))
        if symbols:
            password_chars.append(rnd.choice(string.punctuation))

        remaining_length = length - len(password_chars)
        for _ in range(remaining_length):
            password_chars.append(rnd.choice(chars))

        rnd.shuffle(password_chars)
        password_str = "".join(password_chars)

        if copy:
            try:
                pyperclip.copy(password_str)
                print("Copied!")
            except pyperclip.PyperclipException:
                print("PyPassword ERROR: Error copying password!")

        return password_str

def password_strength(password):
    uppercase_letters = 0
    lowercase_letters = 0
    numbers = 0
    symbols = 0

    for char in password:
        if char.isupper():
            uppercase_letters += 1
        elif char.islower():
            lowercase_letters += 1
        elif char.isdigit():
            numbers += 1
        elif char in strong_chars:
            symbols += 1
        else:
            symbols += 1

    score = 0

    if uppercase_letters > 0:
        score += 1
    if lowercase_letters > 0:
        score += 1
    if numbers > 0:
        score += 1
    if symbols > 0:
        score += 2

    length = len(password)
    if length >= 16:
        score += 3
    elif length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    if score <= 3:
        return "Weak"
    elif 4 <= score <= 5:
        return "Normal"
    elif 6 <= score <= 7:
        return "Strong"
    else:
        return "Very Strong"

def password_input(prompt=""):
    sys.stdout.write(prompt)
    sys.stdout.flush()

    password = ""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch in ("\n", "\r"):
                break
            elif ch == "\x7f":
                if password:
                    password = password[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                password += ch
                sys.stdout.write("*")
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        print()

    return password

def hash_password(password, file_path):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        with open(file_path, "a") as file:
            file.write(hashed_password + "\n")
    except OSError:
        print("PyPassword ERROR: Error saving hashed password!")
        return False

def find_password(password, file_path):
    hashed = hashlib.sha256(password.encode()).hexdigest()

    try:
        with open(file_path, "r") as f:
            for line in f:
                if line.strip() == hashed:
                    return True
        return False
    except FileNotFoundError:
        print("PyPassword ERROR: Error finding password!")
        return False