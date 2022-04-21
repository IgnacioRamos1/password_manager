
import requests
import uuid
import click
from authentication import confirmation
requests.packages.urllib3.disable_warnings()

url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
user = str(uuid.UUID(int=uuid.getnode()))


def change_main_password():
    main_password = click.prompt(
        'Enter new password',
        hide_input=True,
        confirmation_prompt=True
    )
    data = '{"data":{"seed_phrase": "%s"}}' % (main_password)
    requests.post(url, headers=headers, data=data, verify=False)


def change_main_pw():
    vault_stored_seed = requests.get(url, headers=headers, verify=False).json()['data']['data']['seed_phrase']
    
    for _ in range(3):
        seed_input = click.prompt('Enter the 12 words with spaces in between them')

        if seed_input != vault_stored_seed:
            continue
        else:
            change_main_password()
    exit()