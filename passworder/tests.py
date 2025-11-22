import passworder as pwd

#   RANDOM CLASS
pswrd_string = pwd.Random.string_password(12, True, True, True, False, True, 2)
pswrd_number = pwd.Random.number_password(12, False, 2)
pswrd = pwd.Random.password(12, False, True, True, True, False, True, 2)
pswrd_pron = pwd.Random.pronouncable_password(12, True, True, False, False, False, True, 2)
pswrd_custom = pwd.Random.custom_password("ABCDabcd123!", 12, False, 2)

backend = pwd.Backend()

#   GLOBAL FUNCTION
pswrd_input = pwd.password_input("Enter your password: ")

#   BACKEND CLASS
pwd.Backend.brute_force_protection(backend, 2)
pswrd_strength = pwd.Backend.password_strength("F9Distribuion")
pwd.Backend.hash_password(backend, "F9Distribution", "passworderTest.txt")
found_pswrd = pwd.Backend.find_password("F9Distribution", "passworderTest.txt")

print(pswrd_string)
print(pswrd_number)
print(pswrd)
print(pswrd_pron)
print(pswrd_custom)

print(pswrd_input)

print(pswrd_strength)
print(found_pswrd)

