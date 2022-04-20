
import click
from PyInquirer import prompt
from examples import custom_style_2
from select_service import select_service
from add_account import add_new_account
from password_generator import password_generator
from search_username import search_username
from get_accounts import get_all_accounts
from modify import modify
from delete import delete
from connect_database import connect_database
from authentication import user_exists
from login import log_in


def main():
    if user_exists():
        # Llamar a funcion que haga todo esto (NOMBRARLAS BIEN XD)
        options = [
            'Log in',
            'Change main password'
            ]
        questions = [
            {
                'type': 'list',
                'name': 'theme',
                'message': 'It seems you already have an account',
                'choices': options
            }
        ]
        answers = prompt(questions, style=custom_style_2)
        if answers['theme'] == 'Log in':
            authenticated = False
            counter = 0

            while not authenticated and counter < 3:
                counter += 1
                authenticated = log_in()

            if not authenticated:
                print('Too many wrong attempts')
                main()
            else:
                menu()

        elif answers['theme'] == 'Change main password':

            authenticated = False
            counter = 0

            while not authenticated and counter < 3:
                seed_input = click.prompt('Enter the 12 words with spaces in between them')
                counter += 1
                authenticated = change_main_password(seed_input)

            if not authenticated:
                print('Too many wrong attempts')
                main()
            else:
                authenticated = False
                counter = 0

                while not authenticated and counter < 3:
                    counter += 1
                    authenticated, seed = sign_up()

                if not authenticated:
                    print("Too many wrong attempts")
                    main()
                else:
                    print('=========================================================================')
                    print('Save this seed phrase, you will need it to reset your password')
                    print('WARNING: This will be the last time you will see it')
                    print('=========================================================================')
                    print(seed)
                    print('=========================================================================')

                    authenticated = False
                    counter = 0

                    while not authenticated and counter < 3:
                        counter += 1
                        authenticated = log_in()
                    if not authenticated:
                        print('Too many wrong attempts')
                        main()
                    else:
                        menu()

    else:
        # Llamar a funcion que haga todo esto (NOMBRARLAS BIEN XD)
        options = [
            'Sign Up'
            ]
        questions = [
            {
                'type': 'list',
                'name': 'theme',
                'message': 'Welcome!, Please Sing Up.',
                'choices': options
            }
        ]
        answers = prompt(questions, style=custom_style_2)
        if answers['theme'] == 'Sign Up':
            authenticated = False
            counter = 0

            while not authenticated and counter < 3:
                counter += 1
                authenticated, seed = sign_up()

            if not authenticated:
                print("Too many wrong attempts")
                main()
            else:
                print('=========================================================================')
                print('Save this seed phrase, you will need it to reset your password')
                print('WARNING: This will be the last time you will see it')
                print('=========================================================================')
                print(seed)
                print('=========================================================================')

                authenticated = False
                counter = 0

                while not authenticated and counter < 3:
                    counter += 1
                    authenticated = log_in()
                if not authenticated:
                    print('Too many wrong attempts')
                    main()
                else:
                    menu()


def menu():
    collection = connect_database()

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
        select_service(collection)
    elif answers['theme'] == 'Add new account':
        add_new_account(collection)
    elif answers['theme'] == 'Password Generator':
        password_generator()
    elif answers['theme'] == 'Search for a username':
        search_username(collection)
    elif answers['theme'] == 'List of all accounts':
        get_all_accounts(collection)
    elif answers['theme'] == 'Modify an account':
        modify(collection)
    elif answers['theme'] == 'Delete an account':
        delete(collection)


main()
