from cmath import log
import click
import requests
import uuid
from authentication import confirmation
import menu
requests.packages.urllib3.disable_warnings()

url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
user = str(uuid.UUID(int=uuid.getnode()))


def login():
    vault_stored_password = requests.get(url, headers=headers, verify=False).json()['data']['data']['main_password']
    
    for _ in range(3):
        main_password = click.prompt(
        'Enter the main password to access',
        hide_input=True
        )
        if main_password != vault_stored_password:
            continue
        else:
            menu()
    exit()