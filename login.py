
import click
import requests
import uuid
from menu import main_menu
requests.packages.urllib3.disable_warnings()

user = str(uuid.UUID(int=uuid.getnode()))
url_main_password = f'https://18.231.120.197:8200/v1/secret/data/password_manager/user/{user}/main_password'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}


def log_in():
    vault_stored_password = requests.get(url_main_password, headers=headers, verify=False).json()['data']['data']['main_password']

    for attempt in range(3):
        main_password = click.prompt(
            'Enter the main password to access',
            hide_input=True
        )
        print(attempt)
        if attempt == 2:
            print('Too many wrong attempts')
            exit()
        elif main_password != vault_stored_password:
            continue
        else:
            main_menu()
            exit()
