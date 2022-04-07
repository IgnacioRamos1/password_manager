import click
from encrypt import hashing


def add_new_account(collection):
    service = click.prompt('Enter service').capitalize()

    username = click.prompt('Enter username')

    result = collection.find_one({'service': service, 'username': username})

    if result:
        if click.confirm('The user already exists, do you wish to change the password?'):
            modify()
        else:
            menu()
    else:
        password = click.prompt(
                'Enter the password',
                confirmation_prompt=True,
                hide_input=True
                )
        hashed_pasword = hashing(password)

        collection.insert_one(
            {
                'service': service,
                'username': username,
                'password': hashed_pasword
                }
                )
