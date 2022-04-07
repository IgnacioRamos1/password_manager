
import click
import requests
import uuid
from PyInquirer import prompt
from examples import custom_style_2
requests.packages.urllib3.disable_warnings()

url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
user = str(uuid.UUID(int=uuid.getnode()))


def log_in():
    # Ingresar main password para poder acceder al manager
    log_in_password = click.prompt(
        'Enter the main password to access',
        hide_input=True
        )
    r = requests.get(url, headers=headers, verify=False)
    if r.json()['data']['data'][user] == log_in_password:
        print('----------Welcome!---------')
        return True
    else:
        print('The main password is incorrect')
        return False


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
        r = requests.get(url, headers=headers, verify=False)

        for key in r.json()['data']['data'].keys():
            stored_user = key

        if stored_user == user:
            print('The computer is already registered')

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
                # Lo mando al log in
                print('log in')

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
                    info = '{"data":{"%s": "%s"}}' % (user, new_main_password)
                    r = requests.post(
                        url,
                        headers=headers,
                        data=info,
                        verify=False
                        )
                    print('The new password was set correctly')
                    # Lo mando al login

        else:
            info = '{"data":{"%s": "%s"}}' % (user, main_password)
            r = requests.post(url, headers=headers, data=info, verify=False)
            print('The new password was set correctly')
            # Lo mando al log in
    else:
        print("Passwords don't match")
        # Lo hago registrarse de nuevo
