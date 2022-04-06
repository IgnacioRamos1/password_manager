
from PyInquirer import prompt
from examples import custom_style_2
import click
import requests
from select_service import select_service
from add_account import add_new_account
from password_generator import password_generator
from search_username import search_username
from get_accounts import get_all_accounts
from modify import modify
from delete import delete


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
