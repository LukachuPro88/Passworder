import passworder
#import pytest
import tempfile
import sys
from contextlib import redirect_stdout

lengths = [5, 6, 7, 8, 9, 10]
uppercases = [True, False]
lowercases = [True, False]
symbols = [True, False]
copy_flags = [True, False]
utf_8_flags = [True, False]
batch_numbers = [1, 2, 3]
digits_flags = [True, False]
custom_chars_list = ["abcdefg", "hijklmn"]

common_passwords = ["12345", "0000", "abcdefg", "gjksdhfglkajhgf"]


"""
Mock for password_input for CI
"""
def password_input_mock(prompt: str = "", input_string: str = "") -> str:
    return input_string

"""
Mck for _ceck_common_passwords
"""
def _check_common_passwords(password: str) -> bool:
    try:
        with open("common_passwords_cleaned.txt", "r") as file:
            common_passwords = set(line.strip() for line in file if line.strip())

        return password.lower() in common_passwords

    except FileNotFoundError:
        print("common_passwords_cleaned.txt not found!")
        return False

"""
Mock test for brute_force_protection
"""
def test_bruteforce_success(monkeypatch):
    inputs = ["wrong1", "wrong2", "correctPw"]
    iterator = iter(inputs)

    def fake_input(prompt=""):
        return next(iterator)

    monkeypatch.setattr("passworder.password_input", fake_input)

    from io import StringIO
    temp = StringIO()
    sys.stdout = temp

    passworder.Backend.brute_force_protection("correctPw", max_attempts=3)
    sys.stdout = sys.__stdout__

    assert "Access Granted!" in temp.getvalue()


def ci():
    # STRING_PASSWORD
    for length in lengths:
        for upper in uppercases:
            for lower in lowercases:
                for symbol in symbols:
                    for copy_flag in copy_flags:
                        for utf in utf_8_flags:
                            for batch in batch_numbers:
                                with tempfile.TemporaryFile(mode="w+") as f, redirect_stdout(f):
                                    pw_string = passworder.Random.string_password(
                                        length = length,
                                        uppercase = upper,
                                        lowercase = lower,
                                        symbols = symbol,
                                        copy = copy_flag,
                                        utf_8 = utf,
                                        batch_passwords = batch
                                    )
                                assert isinstance(pw_string, str) or isinstance(pw_string, list)

    # NUMBER_PASSWORD
    for length in lengths:
        for copy_flag in copy_flags:
            for batch in batch_numbers:
                with tempfile.TemporaryFile(mode="w+") as f, redirect_stdout(f):
                    pw_num = passworder.Random.number_password(
                        length = length,
                        copy = copy_flag,
                        batch_passwords = batch
                    )
                assert isinstance(pw_num, str) or isinstance(pw_num, list)

    # PASSWORD
    for length in lengths:
        for upper in uppercases:
            for lower in lowercases:
                for symbol in symbols:
                    for copy_flag in copy_flags:
                        for utf in utf_8_flags:
                            for batch in batch_numbers:
                                for digit in digits_flags:
                                    with tempfile.TemporaryFile(mode="w+") as f, redirect_stdout(f):
                                        pw = passworder.Random.password(
                                            length = length,
                                            uppercase = upper,
                                            lowercase = lower,
                                            symbols = symbol,
                                            copy = copy_flag,
                                            utf_8 = utf,
                                            batch_passwords = batch,
                                            digits = digit
                                        )
                                    assert isinstance(pw, str) or isinstance(pw, list)

    # PRONOUNCEABLE_PASSWORD
    for length in lengths:
        for upper in uppercases:
            for lower in lowercases:
                for symbol in symbols:
                    for copy_flag in copy_flags:
                        for utf in utf_8_flags:
                            for batch in batch_numbers:
                                with tempfile.TemporaryFile(mode="w+") as f, redirect_stdout(f):
                                    pw_pronoun = passworder.Random.pronounceable_password(
                                        length = length,
                                        uppercase = upper,
                                        lowercase = lower,
                                        symbols = symbol,
                                        copy = copy_flag,
                                        utf_8 = utf,
                                        batch_passwords = batch
                                    )
                                assert isinstance(pw_pronoun, str) or isinstance(pw_pronoun, list)

    # CUSTOM_PASSWORD
    for char in custom_chars_list:
        for length in lengths:
            for copy_flag in copy_flags:
                for batch in batch_numbers:
                    with tempfile.TemporaryFile(mode="w+") as f, redirect_stdout(f):
                        pw_custom = passworder.Random.custom_password(
                            custom_chars = char,
                            length = length,
                            copy = copy_flag,
                            batch_passwords = batch
                        )
                    assert isinstance(pw_custom, str) or isinstance(pw_custom, list)

    # PASSWORD_INPUT
    prompt = "Enter your password: "
    test_pw = "SuperSecret123!"
    result = password_input_mock(prompt=prompt, input_string=test_pw)
    assert result == test_pw

    # HASH_PASSWORD
    test_pw = "SuperSecretPassword123!"
    with tempfile.NamedTemporaryFile(mode="w+", delete=True) as tmp:
        tmp_path = tmp.name

    success = passworder.Backend.hash_password(test_pw, tmp_path)
    assert success is True

    with open(tmp_path, "r") as tmp:
        content = tmp.read().strip()
        assert len(content) > 0
        assert content != test_pw

    # FIND_PASSWORD
    test_pw2 = "SuperSecretPassword123"
    passworder.Backend.hash_password(test_pw2, tmp_path)

    found_hash = passworder.Backend.find_password(test_pw2, tmp_path)
    assert found_hash is not None
    assert isinstance(found_hash, str)
    assert found_hash != test_pw2
    assert passworder.Backend.ph.verify(found_hash, test_pw2) is True

    # _CHECK_COMMON_PASSWORD
    for i in range(len(common_passwords)):
        pw = common_passwords[i]
        assert _check_common_passwords(pw)

ci()