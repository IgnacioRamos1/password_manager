
import click
import requests
import uuid
from PyInquirer import prompt
from examples import custom_style_2
requests.packages.urllib3.disable_warnings()


def create_account(main_password):
    user = str(uuid.UUID(int=uuid.getnode()))
    data = '{"data":{"user": "%s", "main_password": "%s"}}' % (user, main_password)
    url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
    headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
    requests.post(url, headers=headers, data=data, verify=False)


def get_account(main_password):
    user = str(uuid.UUID(int=uuid.getnode()))
    url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
    headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
    account = requests.get(url, headers=headers, verify=False)

    return account.json()['data']['data']['user'] == user and account.json()['data']['data']['main_password'] == main_password
    

def check_if_user_exists():
    user = str(uuid.UUID(int=uuid.getnode()))
    url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
    headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
    account = requests.get(url, headers=headers, verify=False)

    return account.json()['data']['data']['user'] == user


def log_in():
    main_password = click.prompt(
        'Enter the main password to access',
        hide_input=True
        )

    return get_account(main_password)


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

        if not get_account(main_password):

            # Ofrecer opcion cambiar password o loguearse

            options = [
                'Log In',
                'Change main Password'
                ]
            questions = [
                {
                    'type': 'list',
                    'name': 'theme',
                    'message': 'How do you wish to proceed?',
                    'choices': options
                }
            ]
            answers = prompt(questions, style=custom_style_2)
            if answers['theme'] == 'Log In':
                return True

            elif answers['theme'] == 'Change main Password':
                new_main_password = click.prompt(
                    'New password (must contain 32 characters)',
                    hide_input=True
                    )

                while len(new_main_password) != 32:
                    new_main_password = click.prompt(
                        'New passowrd (must contain 32 characters)',
                        hide_input=True
                        )

                new_main_password_2 = click.prompt(
                    'Confirm password',
                    hide_input=True
                    )

                if new_main_password == new_main_password_2:
                    create_account(main_password)
                    print('The new password was set correctly')
                    return True

        else:
            create_account(main_password)
            print('The new password was set correctly')
            return True
    else:
        print("Passwords don't match")
        return False

def change_main_password():
    return
