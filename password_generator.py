import random as rand
import re
from strength_checker import check_password_strength

#Possible characters
all_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

def generate_random_password():
    length = rand.randint(13, 20) #Random length between 13 and 20
    password = ''.join(rand.choice(all_chars) for _ in range(length)) #Random password generation

    return password

def create_password():
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$'

    while True:
        p = input("Enter your password: ")
        if re.match(pattern, p):
            print("Password is strong.")
            return p
        else:
            print("Password is weak. It must contain at least one uppercase letter, one digit, and one special character.")



def main():
    q = input("Do you want to 1. generate a random password or 2. check your own password?: (1 or 2) ")
    if q== '1':
        password = generate_random_password()
        print(f"Generated password: {password}")
        strength = check_password_strength(password)
        print(f"Password strength: {strength}")

    elif q == '2':
        password = create_password()
        if password is None:
            print("Password creation failed.")
            return
        strength = check_password_strength(password)
        print(f"Password strength: {strength}")

if __name__ == "__main__":
    main()