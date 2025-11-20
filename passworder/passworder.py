import secrets
import string
import pyperclip
import sys
import hashlib
from typing import Union, List, Optional

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
    def string_password(length:int, uppercase:bool=True, lowercase:bool=True,
                        symbols:bool=True, copy:bool=True, utf_8:bool=False,
                        batch_passwords:int=1) -> Union[str,List[str]]:
        #   GENERATE A RANDOM PASSWORD WITH LETTERS ONLY

        def _generate_one() -> str:
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
            pw_list = [_generate_one() for _ in range(batch_passwords)]
            return pw_list
    

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
            pw_list = [_generate_one() for _ in range(batch_passwords)]
            return pw_list

    @staticmethod
    def password(length:int, uppercase:bool=True, lowercase:bool=True,
                 symbols:bool=True,digits:bool=True,copy:bool=True,
                 utf_8:bool=False,batch_passwords:int=1) -> Union[str,List[str]]:
        def _generate_one() -> str:
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
    def pronouncable_password(length:int, uppercase:bool=True, lowercase:bool=True,
                              symbols:bool=True,digits:bool=True,copy:bool=True,
                              utf_8:bool=False,batch_passwords:int=1) -> Union[str,List[str]]:
        def _generate_one() -> str:     
            while True:
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

class Backend:
    #   BACKEND FUNCTIONS
    def __init__(self, password: Optional[str] = None, found: bool = True, data: Optional[str] = None):
        self.password = password
        self.found = found
        self.data = data

    def brute_force_protection(self, max_attempts: int = 3):
        if not self.found or self.password is None:
            print("Password not found — brute force protection disabled.")
            return self

        attempts = 0
        while attempts < max_attempts:
            user_input = password_input("Enter Password: ")
            if user_input == self.password:
                print("Access Granted!")
                return self
            else:
                attempts += 1
                print(f"Incorrect Password! {max_attempts - attempts} attempts left.")

        print("Access Denied!")
        return self

    def __str__(self):
        return self.password if self.password is not None else "NOT FOUND"


    @staticmethod
    def password_strength(password:str) -> str:
        #   CALCULATE PASSWORD STRENGTH
        uppercase_letters = 0
        lowercase_letters = 0
        numbers = 0
        symbols = 0

        for char in password:
            if char in utf_8_upper:
                uppercase_letters += 1
            elif char in utf_8_lower:
                lowercase_letters += 1
            elif char.isupper():
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
        
    @staticmethod
    def hash_password(password:str,file_path:str) -> Optional[bool]:
        #   HASH A PASSWORD
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            with open(file_path, "a") as file:
                file.write(hashed_password + "\n")
            return True
        except OSError:
            print("Passworder ERROR: Error saving hashed password!")
            return False
        
    @staticmethod
    def find_password(password: str, file_path: str):
        try:
            with open(file_path, "r") as file:
                for line in file:
                    if password in line:
                        return Backend(password=password, found=True, data=line.strip())
        except FileNotFoundError:
            pass

        return Backend(password=None, found=False)

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