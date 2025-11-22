import secrets
import string
import pyperclip
import sys
from argon2 import PasswordHasher, exceptions
from typing import Union, List, Optional

"""
passworder.py

Passworder is a Python package that has utilities for password management, generation,
and security
"""

"""

Global Constants

"""
UTF_8_UPPER = "ÄÖÅ"                                         #   CONSTANT
UTF_8_LOWER = "äöå"                                         #   CONSTANT
UTF_8_CHARS = UTF_8_UPPER + UTF_8_LOWER                     #   CONSTANT
STRONG_CHARS = string.punctuation                           #   CONSTANT
VOWELS = "AEIOUYÄÖÅaeiouyäöå"                               #   CONSTANT
CONSONANTS = "BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz"   #   CONSTANT

"""

Platform-specific imports

"""
if sys.platform == "win32":
    import msvcrt   #   WINDOWS
else:
    import tty      #   LINUX / MACOS
    import termios


"""
Random has tools for generating random passwords. 
Random helps you customize passwords to your liking.

"""

class Random:

    """

    string_password:
        Generate a random password with letters only.
    """
    @staticmethod
    def string_password(length:int, uppercase:bool=True, lowercase:bool=True,
                        symbols:bool=True, copy:bool=True, utf_8:bool=False,
                        batch_passwords:int=1) -> Union[str,List[str]]:

        def _generate_one() -> str:
            chars = ""
            if uppercase:
                chars += string.ascii_uppercase
                if utf_8:
                    chars += UTF_8_UPPER
            if lowercase:
                chars += string.ascii_lowercase
                if utf_8:
                    chars += UTF_8_LOWER
            if symbols:
                chars += string.punctuation
            if not chars:
                chars = string.ascii_letters

            password_chars = []
            if uppercase:
                password_chars.append(secrets.choice(string.ascii_uppercase + (UTF_8_UPPER if utf_8 else "")))
            if lowercase:
                password_chars.append(secrets.choice(string.ascii_lowercase + (UTF_8_LOWER if utf_8 else "")))
            if symbols:
                password_chars.append(secrets.choice(string.punctuation))
            if utf_8:
                password_chars.append(secrets.choice(UTF_8_CHARS))

            remaining_length = max(length - len(password_chars), 0)
            for _ in range(remaining_length):
                password_chars.append(secrets.choice(chars))

            while True:
                password_chars = _secure_shuffle(password_chars)
                if _avoid_repeats("".join(password_chars)):
                    break

            return "".join(password_chars)

        if batch_passwords == 1:
            pw = _generate_one()
            if copy:
                try:
                    pyperclip.copy(pw)
                    print("Copied!")
                except pyperclip.PyperclipException:
                    print("Error copying password!")
            return pw
        else:
            return [_generate_one() for _ in range(batch_passwords)]

    @staticmethod
    def number_password(length:int, copy:bool=True, batch_passwords:int=1) -> Union[str,List[str]]:
        def _generate_one() -> str:
            while True:
                password_chars = [str(secrets.randbelow(10)) for _ in range(length)]
                if _avoid_repeats("".join(password_chars)):
                    break
            return "".join(password_chars)

        if batch_passwords == 1:
            pw = _generate_one()
            if copy:
                try:
                    pyperclip.copy(pw)
                    print("Copied!")
                except pyperclip.PyperclipException:
                    print("Error copying password!")
            return pw
        else:
            return [_generate_one() for _ in range(batch_passwords)]

    @staticmethod
    def password(length:int, uppercase:bool=True, lowercase:bool=True,
                 symbols:bool=True,digits:bool=True,copy:bool=True,
                 utf_8:bool=False,batch_passwords:int=1) -> Union[str,List[str]]:

        def _generate_one() -> str:
            chars = ""
            if uppercase:
                chars += string.ascii_uppercase
                if utf_8:
                    chars += UTF_8_UPPER
            if lowercase:
                chars += string.ascii_lowercase
                if utf_8:
                    chars += UTF_8_LOWER
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
                password_chars.append(secrets.choice(UTF_8_CHARS))

            remaining_length = max(length - len(password_chars), 0)
            for _ in range(remaining_length):
                password_chars.append(secrets.choice(chars))

            while True:
                password_chars = _secure_shuffle(password_chars)
                if _avoid_repeats("".join(password_chars)):
                    break

            return "".join(password_chars)

        if batch_passwords == 1:
            pw = _generate_one()
            if copy:
                try:
                    pyperclip.copy(pw)
                    print("Copied!")
                except pyperclip.PyperclipException:
                    print("Passworder ERROR: Error copying password!")
            return pw
        else:
            return [_generate_one() for _ in range(batch_passwords)]

    @staticmethod
    def pronounceable_password(length:int, uppercase:bool=True, lowercase:bool=True,
                              symbols:bool=True,digits:bool=True,copy:bool=True,
                              utf_8:bool=False,batch_passwords:int=1) -> Union[str,List[str]]:

        def _generate_one() -> str:
            while True:
                password_chars = []
                use_consonant = True

                while len(password_chars) < length:
                    if use_consonant:
                        char_pool = CONSONANTS
                        if utf_8 and uppercase:
                            char_pool += UTF_8_UPPER
                        elif utf_8 and lowercase:
                            char_pool += UTF_8_LOWER
                    else:
                        char_pool = VOWELS
                        if utf_8 and uppercase:
                            char_pool += UTF_8_UPPER
                        elif utf_8 and lowercase:
                            char_pool += UTF_8_LOWER

                    if char_pool:
                        password_chars.append(secrets.choice(char_pool))
                    use_consonant = not use_consonant

                extras = []
                if digits:
                    extras.append(secrets.choice(string.digits))
                if symbols:
                    extras.append(secrets.choice(string.punctuation))

                password_chars += extras
                password_chars = _secure_shuffle(password_chars)
                password_str = "".join(password_chars[:length])

                if _avoid_repeats(password_str):
                    return password_str

        if batch_passwords == 1:
            pw = _generate_one()
            if copy:
                try:
                    pyperclip.copy(pw)
                    print("Copied!")
                except pyperclip.PyperclipException:
                    print("Passworder ERROR: Error copying password!")
            return pw
        else:
            return [_generate_one() for _ in range(batch_passwords)]


    """
    custom_password:
        Generate a random password with custom characters only.
    """
    @staticmethod
    def custom_password(custom_chars:Union[str,List[str]], length:int,
                        copy:bool=True, batch_passwords:int=1) -> Union[str,List[str]]:
        #   GENERATE A RANDOM PASSWORD WITH CUSTOM CHARACTERS ONLY

        def _generate_one() -> str:
            while True:
                password_chars = [secrets.choice(custom_chars) for _ in range(length)]
                if _avoid_repeats("".join(password_chars)):
                    break
            return "".join(password_chars)

        if batch_passwords == 1:
            pw = _generate_one()
            if copy:
                try:
                    pyperclip.copy(pw)
                    print("Copied!")
                except pyperclip.PyperclipException:
                    print("Passworder ERROR: Error copying password!")
            return pw
        else:
            pw_list = [_generate_one() for _ in range(batch_passwords)]
            return pw_list
"""
password_input:
    Get a hidden password input from the user.
"""
def password_input(prompt:str="") -> str:
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
                except UnicodeDecodeError:
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

"""
Backend class handles password hashing, finding, and brute-force protection.
"""
class Backend:
    #   BACKEND FUNCTIONS

    ph = PasswordHasher()  # single shared hasher

    """
    brute_force_protection:
        Implement brute-force protection by limiting password attempts.
    """
    @staticmethod
    def brute_force_protection(password: str, max_attempts: int = 3):
        if not password:
            print("Password not found — brute force protection disabled.")
            return

        attempts = 0
        while attempts < max_attempts:
            user_input = password_input("Enter Password: ")
            if user_input == password:
                print("Access Granted!")
                return
            else:
                attempts += 1
                print(f"Incorrect Password! {max_attempts - attempts} attempts left.")

        print("Access Denied!")

    """
    password_strength:
        Evaluate the strength of a given password.
    """
    @staticmethod
    def password_strength(password: str) -> str:
        uppercase_letters = 0
        lowercase_letters = 0
        numbers = 0
        symbols = 0

        for char in password:
            if char in UTF_8_UPPER:
                uppercase_letters += 1
            elif char in UTF_8_LOWER:
                lowercase_letters += 1
            elif char.isupper():
                uppercase_letters += 1
            elif char.islower():
                lowercase_letters += 1
            elif char.isdigit():
                numbers += 1
            elif char in STRONG_CHARS:
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

    """
    hash_password:
        Hash a password and save it to a file.
    """
    @staticmethod
    def hash_password(password: str, file_path: str) -> Optional[bool]:
        try:
            hashed_password = Backend.ph.hash(password)
            with open(file_path, "a") as file:
                file.write(hashed_password + "\n")
            return True
        except (OSError, exceptions.HashingError) as e:
            print(f"Passworder ERROR: Could not hash/save password! ({e})")
            return False

    """
    find_password:
        Find a hashed password in a file.
    """
    @staticmethod
    def find_password(password: str, file_path: str) -> Optional[str]:
        ph = Backend.ph
        try:
            with open(file_path, "r") as file:
                for line in file:
                    hashed = line.strip()
                    try:
                        if ph.verify(hashed, password):
                            return hashed
                    except exceptions.VerifyMismatchError:
                        continue
        except FileNotFoundError:
            return None

        return None


#   INTERNAL FUNCTIONS
def _avoid_repeats(password:str,max_repeat:int=3) -> bool:
    count = 1
    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            count += 1
            if count > max_repeat:
                return False
        else:
            count = 1
    return True

def _secure_shuffle(chars:Union[str,List[str]]) -> Union[str,List[str]]:
    is_string = isinstance(chars, str)
    lst = list(chars)

    for i in range(len(lst) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        lst[i], lst[j] = lst[j], lst[i]

    return "".join(lst) if is_string else lst
