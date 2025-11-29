import passworder
import sys
from contextlib import redirect_stdout
from itertools import product
import tempfile

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

def password_input_mock(prompt: str = "", input_string: str = "") -> str:
    return input_string

with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
    tmp_path = tmp.name
    for pw in ["12345", "0000", "abcdefg", "gjksdhfglkajhgf"]:
        tmp.write(pw + "\n")

def _check_common_passwords(password):
    with open(tmp_path, "r") as f:
        common_set = set(line.strip() for line in f if line.strip())
    return password.lower() in common_set

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
    for length, upper, lower, symbol, copy_flag, utf, batch in product(
            lengths,
            uppercases,
            lowercases,
            symbols,
            copy_flags,
            utf_8_flags,
            batch_numbers
    ):
        with tempfile.TemporaryFile(mode="w+") as f, redirect_stdout(f):
            pw_string = passworder.Random.string_password(
                length=length,
                uppercase=upper,
                lowercase=lower,
                symbols=symbol,
                copy=copy_flag,
                utf_8=utf,
                batch_passwords=batch
            )
        assert isinstance(pw_string, (str, list))

    for length, copy_flag, batch in product(
            lengths,
            copy_flags,
            batch_numbers
    ):
        with tempfile.TemporaryFile(mode="w+") as f, redirect_stdout(f):
            pw_num = passworder.Random.number_password(
                length=length,
                copy=copy_flag,
                batch_passwords=batch
            )
        assert isinstance(pw_num, (str, list))

    for length, upper, lower, symbol, copy_flag, utf, batch, digit in product(
            lengths,
            uppercases,
            lowercases,
            symbols,
            copy_flags,
            utf_8_flags,
            batch_numbers,
            digits_flags
    ):
        with tempfile.TemporaryFile(mode="w+") as f, redirect_stdout(f):
            pw = passworder.Random.password(
                length=length,
                uppercase=upper,
                lowercase=lower,
                symbols=symbol,
                copy=copy_flag,
                utf_8=utf,
                batch_passwords=batch,
                digits=digit
            )
        assert isinstance(pw, (str, list))

    for length, upper, lower, symbol, copy_flag, utf, batch in product(
            lengths,
            uppercases,
            lowercases,
            symbols,
            copy_flags,
            utf_8_flags,
            batch_numbers
    ):
        with tempfile.TemporaryFile(mode="w+") as f, redirect_stdout(f):
            pw_pronoun = passworder.Random.pronounceable_password(
                length=length,
                uppercase=upper,
                lowercase=lower,
                symbols=symbol,
                copy=copy_flag,
                utf_8=utf,
                batch_passwords=batch
            )
        assert isinstance(pw_pronoun, (str, list))

    for char, length, copy_flag, batch in product(
            custom_chars_list,
            lengths,
            copy_flags,
            batch_numbers
    ):
        with tempfile.TemporaryFile(mode="w+") as f, redirect_stdout(f):
            pw_custom = passworder.Random.custom_password(
                custom_chars=char,
                length=length,
                copy=copy_flag,
                batch_passwords=batch
            )
        assert isinstance(pw_custom, (str, list))

    prompt = "Enter your password: "
    test_pw = "SuperSecret123!"
    result = password_input_mock(prompt=prompt, input_string=test_pw)
    assert result == test_pw

    test_pw = "SuperSecretPassword123!"
    with tempfile.NamedTemporaryFile(mode="w+", delete=True) as tmp:
        tmp_path = tmp.name

    success = passworder.Backend.hash_password(test_pw, tmp_path)
    assert success is True

    with open(tmp_path, "r") as tmp:
        content = tmp.read().strip()
        assert len(content) > 0
        assert content != test_pw

    test_pw2 = "SuperSecretPassword123"
    passworder.Backend.hash_password(test_pw2, tmp_path)

    found_hash = passworder.Backend.find_password(test_pw2, tmp_path)
    assert found_hash is not None
    assert isinstance(found_hash, str)
    assert found_hash != test_pw2
    assert passworder.Backend.ph.verify(found_hash, test_pw2) is True

    for i in range(len(common_passwords)):
        pw = common_passwords[i]
        assert _check_common_passwords(pw)

ci()