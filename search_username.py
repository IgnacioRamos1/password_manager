import click
from decrypt import decrypt


def search_username(collection):
    username = click.prompt('Enter the username you wish to search')

    accounts = list(collection.find({'username': username}))

    if len(accounts) == 0:
        print("That username doesn't exist")
    else:
        for account in accounts:
            service = account['service']
            password = account['password']
            hashed_pasword = decrypt(password)

        print('----------------------')
        print(f'---- {service} ----')
        print(f'User  | {username}')
        print(f'Password | {hashed_pasword}')
