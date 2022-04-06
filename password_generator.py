import click
import random
import string


def password_generator():
    length = click.prompt('Enter the length of the password', type=int)

    if click.confirm('Do you wish it to contain symbols?'):
        # Con simbolos
        characters = list(string.ascii_letters + string.digits + '!@#$%^&*()')
        random.shuffle(characters)
        password = []
        for i in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        print(''.join(password))

    else:
        # Sin simbolos
        characters = list(string.ascii_letters + string.digits)
        random.shuffle(characters)
        password = []
        for i in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        print(''.join(password))
