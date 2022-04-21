import click
from decrypt import decrypt


def select_service(collection):
    search = click.prompt(
        'Enter the service you want to search'
        ).capitalize()
    result = list(collection.find({'service': search}))

    if len(result) == 0:
        # No existen cuentas para ese servicio
        print('There are not accounts for that service')
    else:
        for account in result:
            plain_text_password = decrypt(account['password'])
            print('----------------------------')
            print(f'User     | {account["username"]}')
            print(f'Password | {plain_text_password}')
