
from PyInquirer import prompt
from examples import custom_style_2
from cryptography.fernet import Fernet
import base64
from pymongo import MongoClient
import random
import string
import click
import requests


cluster = MongoClient(
    'mongodb+srv://IgnacioRamos:TZxa68aDGrWWVUeq@cluster0.tzlxj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    )
db = cluster['password_manager']
collection = db['accounts']

main_password = 'E2d25dSpas5NNHNE7fq5NCZSF6RTadtk'


def sign_up():

    main_password = click.prompt(
        'New password (must contain 32 characters)',
        hide_input=True
        )

    while len(main_password) != 32:
        main_password = click.prompt(
            'New passowrd (must contain 32 characters)', 
            hide_input=True
            )

    main_password_2 = click.prompt('Confirm password', hide_input=True)

    if main_password == main_password_2:
        url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
        headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
        info = '{"data":{"user": "%s"}}' % (main_password)

        r = requests.post(url, headers=headers, data=info, verify=False)

        print(r.json())
        print('The new password was set correctly')

        log_in()

    else:
        print("Passwords don't match")
        return 'error'


def log_in():
    # Ingresar main password para poder acceder al manager
    log_in_password = click.prompt(
        'Enter the main password to access',
        hide_input=True
        )

    url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
    headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
    r = requests.get(url, headers=headers, verify=False)
    print(r.json())
    if r.json()['data']['data']['user'] == log_in_password:
        print('Welcome!')
        menu()
    else:
        print('The main password is incorrect')
        return 'error'


def menu():
    options = [
        'Select service',
        'Add new account',
        'Password Generator',
        'Search for a username',
        'List of all accounts',
        'Modify an account',
        'Delete an account'
        ]
    questions = [
        {
            'type': 'list',
            'name': 'theme',
            'message': 'What do you want to do?',
            'choices': options
        }
    ]
    answers = prompt(questions, style=custom_style_2)
    if answers['theme'] == 'Select service':
        select_service()
    elif answers['theme'] == 'Add new account':
        add_new_account()
    elif answers['theme'] == 'Password Generator':
        password_generator()
    elif answers['theme'] == 'Search for a username':
        search_username()
    elif answers['theme'] == 'List of all accounts':
        get_all_accounts()
    elif answers['theme'] == 'Modify an account':
        modify()
    elif answers['theme'] == 'Delete an account':
        delete()

# ------------------------------------------------------


def select_service():
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
            print(f'User  | {account["username"]}')
            print(f'Password | {plain_text_password}')


def hashing(password):
    key = base64.urlsafe_b64encode(main_password.encode('utf-8'))
    f = Fernet(key)
    hashed_pasword = f.encrypt(password.encode())
    return hashed_pasword


def decrypt(password):
    key = base64.urlsafe_b64encode(main_password.encode('utf-8'))
    f = Fernet(key)
    plain_text_password = (f.decrypt(password)).decode('utf-8')
    return plain_text_password


def add_new_account():
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


def search_username():
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


def get_all_accounts():
    accounts = collection.find({})
    for account in accounts:
        service = account['service']
        username = account['username']
        password = account['password']

        plain_text_password = decrypt(password)

        print('---------------------------')
        print(f'Servicio | {service}')
        print(f'Usuario  | {username}')
        print(f'Password | {plain_text_password}')


def modify():
    service = click.prompt(
         'Enter the service'
         ).capitalize()
    services = list(collection.find({'service': service}))

    if len(services) == 0:
        print(f'The service: {service} is not found in the data base')
    else:
        options = [
            'User',
            'Password'
        ]

        questions = [
            {
                'type': 'list',
                'name': 'theme',
                'message': 'What do you want to do?',
                'choices': options
            }
                ]
        answers = prompt(questions, style=custom_style_2)

        if answers['theme'] == 'User':
            old_user = click.prompt('Enter the username of the account')
            accounts = list(collection.find(
                {
                    'service': service,
                    'username': old_user
                }))

            if len(accounts) == 0:
                print(
                        f'The user: {old_user} was not found in the service: {service}'
                    )
            else:
                new_user = click.prompt('Enter the new username')

                if click.confirm(f'\nAre you sure you want to modify the user?\n{old_user} --> {new_user}'):

                    collection.find_one_and_update(
                        {
                            'service': service,
                            'username': old_user
                        },
                        {
                            '$set': {'username': new_user}
                        })
                    print('The username was updated correctly')

                else:
                    print('The operation was cancelled')

        elif answers['theme'] == 'Password':
            old_user = click.prompt('Enter the username of the account')
            account = list(collection.find(
                {
                    'service': service,
                    'username': old_user
                }))

            if len(account) == 0:
                print(f'The user: {old_user} was not found in the service: {service}')
            else:
                new_password = click.prompt(
                        'Enter the new password',
                        confirmation_prompt=True,
                        hide_input=True
                        )

                if click.confirm('Are you sure you want to modify the password?'):
                    hashed_pasword = hashing(new_password)

                    collection.find_one_and_update(
                        {
                            'service': service,
                            'username': old_user
                        },
                        {
                            '$set': {'password': hashed_pasword}
                        })
                    print('The password was updated correctly')

                else:
                    print('The operation was cancelled')


def delete():
    service = click.prompt('Enter the service').capitalize()

    services = list(collection.find({'service': service}))

    if len(services) == 0:
        print(f'The service: {service} was not found in the data base')
    else:
        user = click.prompt('Enter the username you wish to delete')
        accounts = list(collection.find(
            {
                'service': service,
                'username': user
            }))

        if len(accounts) == 0:
            print(f'There is no username: {user} in the service: {service}')

        else:
            if click.confirm('The account was found! \nAre you sure you want to delete it?'):
                collection.find_one_and_delete(
                    {
                        'service': service,
                        'username': user
                    })
                print('The account was deleted correctly')
            else:
                print('The operation was cancelled')


# Si el tipo tiene ya una cuenta:
# log_in()
    # error = log_in()
    # if error = 'error':
        # lo mando de vuelta a la pagina principal
    # else:
    #   menu()

# Si no tiene una cuenta:
# sing_up()

    # error = sign_up()
    # if error = 'error':
        # lo mando de vuelta a la pagina principal
    # else:
    #   log_in()

menu()
