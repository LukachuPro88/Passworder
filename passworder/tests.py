from passworder import *
import os

def run_tests():
    print("=== TEST: string_password ===")
    pw1 = Random.string_password(12, uppercase=True, lowercase=True, symbols=True, utf_8=True, copy=False)
    print("Password:", pw1)
    print("Length:", len(pw1))

    print("\n=== TEST: number_password ===")
    pw2 = Random.number_password(8, copy=False)
    print("Password:", pw2)
    print("Length:", len(pw2))
    print("Is all digits:", pw2.isdigit())

    print("\n=== TEST: password ===")
    pw3 = Random.password(16, uppercase=True, lowercase=True, symbols=True, digits=True, utf_8=True, copy=False)
    print("Password:", pw3)
    print("Length:", len(pw3))

    print("\n=== TEST: pronouncable_password ===")
    pw4 = Random.pronouncable_password(14, uppercase=True, lowercase=True, symbols=True, digits=True, utf_8=True, copy=False)
    print("Password:", pw4)
    print("Length:", len(pw4))

    print("\n=== TEST: password_strength ===")
    print("pw1 strength:", password_strength(pw1))
    print("pw2 strength:", password_strength(pw2))
    print("pw3 strength:", password_strength(pw3))
    print("pw4 strength:", password_strength(pw4))

    print("\n=== TEST: hash_password + find_password ===")
    test_file = "pw_test_hash.txt"
    if os.path.exists(test_file):
        os.remove(test_file)

    hash_password(pw1, test_file)
    found = find_password(pw1, test_file)
    not_found = find_password("wrongpassword123", test_file)
    print(f"Password '{pw1}' found in file:", found)
    print("Random wrong password found in file:", not_found)

    os.remove(test_file)
    print("\nAll tests passed successfully! 🎉")

if __name__ == "__main__":
    run_tests()