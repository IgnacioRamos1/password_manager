import click
import requests
import uuid
from authentication import confirmation
requests.packages.urllib3.disable_warnings()

url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
user = str(uuid.UUID(int=uuid.getnode()))


def get_account(main_password):
    account = requests.get(url, headers=headers, verify=False)
    return account.json()['data']['data']['user'] == user and account.json()['data']['data']['main_password'] == main_password


def login_input():
    main_password = click.prompt(
        'Enter the main password to access',
        hide_input=True
        )

    return get_account(main_password), None


def login():
    authenticated, _ = confirmation(login_input, 0)
    return authenticated
