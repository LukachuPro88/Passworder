import secrets
import random as rnd
import string
import pyperclip
import sys
import hashlib

utf_8_upper = "ÄÖÅ"
utf_8_lower = "äöå"
utf_8_chars = utf_8_upper + utf_8_lower

vowels = "aeiouyäöåAEIOUYÄÖÅ"
consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"

if sys.platform == "win32":
    import msvcrt   #   WINDOWS
else:
    import tty      #   LINUX / MACOS
    import termios

strong_chars = string.punctuation

class Random:
    @staticmethod
    def string_password(length, uppercase=True, lowercase=True, symbols=True, copy=True, utf_8=False):
        #   GENERATE A RANDOM PASSWORD WITH ONLY STRINGS
        chars = ""
    
        if uppercase:
            chars += string.ascii_uppercase
            if utf_8:
                chars += utf_8_upper
        if lowercase:
            chars += string.ascii_lowercase
            if utf_8:
                chars += utf_8_lower
        if symbols:
            chars += string.punctuation

        if not chars:
            chars = string.ascii_letters

        password_chars = []
        if uppercase:
            password_chars.append(secrets.choice(string.ascii_uppercase + (utf_8_upper if utf_8 else "")))
        if lowercase:
            password_chars.append(secrets.choice(string.ascii_lowercase + (utf_8_lower if utf_8 else "")))
        if symbols:
            password_chars.append(secrets.choice(string.punctuation))
        if utf_8:
            password_chars.append(secrets.choice(utf_8_chars))

        remaining_length = max(length - len(password_chars), 0)
        for _ in range(remaining_length):
            password_chars.append(secrets.choice(chars))

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
        #   GENERATE A RANDOM PASSWORD WITH ONLY NUMBERS
        password_chars = [str(secrets.randbelow(10)) for _ in range(length)]
        password_str = "".join(password_chars)

        if copy:
            try:
                pyperclip.copy(password_str)
                print("Copied!")
            except pyperclip.PyperclipException:
                print("Error copying password!")

        return password_str

    @staticmethod
    def password(length, uppercase=True, lowercase=True, symbols=True, digits=True, copy=True, utf_8=False):
        #   GENERATE A RANDOM PASSWORD INCLUDING EVERYTHING
        chars = ""
        if uppercase:
            chars += string.ascii_uppercase
            if utf_8:
                chars += utf_8_upper
        if lowercase:
            chars += string.ascii_lowercase
            if utf_8:
                chars += utf_8_lower
        if symbols:
            chars += string.punctuation
        if digits:
            chars += string.digits
        if not chars:
            chars = string.ascii_letters

        password_chars = []
        if uppercase:
            password_chars.append(secrets.choice(string.ascii_uppercase))
        if lowercase:
            password_chars.append(secrets.choice(string.ascii_lowercase))
        if digits:
            password_chars.append(secrets.choice(string.digits))
        if symbols:
            password_chars.append(secrets.choice(string.punctuation))
        if utf_8:
            password_chars.append(secrets.choice(utf_8_chars))

        remaining_length = max(length - len(password_chars), 0)
        for _ in range(remaining_length):
            password_chars.append(secrets.choice(chars))

        rnd.shuffle(password_chars)
        password_str = "".join(password_chars)

        if copy:
            try:
                pyperclip.copy(password_str)
                print("Copied!")
            except pyperclip.PyperclipException:
                print("Passworder ERROR: Error copying password!")

        return password_str
    
    @staticmethod
    def pronouncable_password(length, uppercase=True, lowercase=True, symbols=True, digits=True, copy=True, utf_8=False):
        #   GENERATE A PRONOUNCABLE PASSWORD template(CVCVCV) C = Consonant, V = Vowel
        password_chars = []
        use_consonant = True

        while len(password_chars) < length:
            char_pool = ""
            if use_consonant:
                char_pool = consonants
                if utf_8 and uppercase:
                    char_pool += utf_8_upper
                elif utf_8 and lowercase:
                    char_pool += utf_8_lower
            else:
                char_pool = vowels
                if utf_8 and uppercase:
                    char_pool += utf_8_upper
                elif utf_8 and lowercase:
                    char_pool += utf_8_lower

            if char_pool:
                password_chars.append(secrets.choice(char_pool))
            use_consonant = not use_consonant

        extras = []
        if digits:
            extras.append(secrets.choice(string.digits))
        if symbols:
            extras.append(secrets.choice(string.punctuation))

        password_chars += extras

        password_str = "".join(password_chars[:length])

        if copy:
            try:
                pyperclip.copy(password_str)
                print("Copied!")
            except pyperclip.PyperclipException:
                print("Passworder ERROR: Error copying password!")

        return password_str

def password_strength(password):
    #   CALCULATE PASSWORD STRENGTH
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
    #   GET A HIDDEN PASSWORD INPUT
    sys.stdout.write(prompt)
    sys.stdout.flush()
    password = ""
    if sys.platform == "win32":

        #   WINDOWS
        while True:
            ch = msvcrt.getch()
            if ch in {b"\r", b"\n"}:
                break
            elif ch in {b"\x08", b"\x7f"}:
                if password:
                    password = password[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                try:
                    char = ch.decode()
                except:
                    continue
                password += char
                sys.stdout.write("*")
                sys.stdout.flush()
        print()
        return password
    else:

        # LINUX / MACOS
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
    #   HASH A PASSWORD
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        with open(file_path, "a") as file:
            file.write(hashed_password + "\n")
    except OSError:
        print("Passworder ERROR: Error saving hashed password!")
        return False

def find_password(password, file_path):
    #   FIND A PASSWORD
    hashed = hashlib.sha256(password.encode()).hexdigest()
    try:
        with open(file_path, "r") as f:
            for line in f:
                if line.strip() == hashed:
                    return True
        return False
    except FileNotFoundError:
        print("Passworder ERROR: Error finding password!")
        return False