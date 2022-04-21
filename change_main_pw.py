
import requests
import uuid
import click
from authentication import confirmation
requests.packages.urllib3.disable_warnings()

url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
user = str(uuid.UUID(int=uuid.getnode()))


def check_seed(seed):
    account = requests.get(url, headers=headers, verify=False)
    return account.json()['data']['data']['seed_phrase'] == seed


def get_seed():
    seed_input = click.prompt('Enter the 12 words with spaces in between them')
    return check_seed(seed_input), None


def change_main_password_input():
    main_password = click.prompt(
        'Enter new password',
        hide_input=True,
        confirmation_prompt=True
        )

    if main_password:
        account = requests.get(url, headers=headers, verify=False)
        seed = account.json()['data']['data']['seed_phrase']
        data = '{"data":{"user": "%s", "main_password": "%s", "seed_phrase": "%s", "main_hashing_pw": "E2d25dSpas5NNHNE7fq5NCZSF6RTadtk"}}' % (user, main_password, seed)
        requests.post(url, headers=headers, data=data, verify=False)
        return True, None
    else:
        return False, None


def change_main_password():
    authenticated_get_seed, _ = confirmation(get_seed, 0)
    authenticated_main_password, _ = confirmation(change_main_password_input, 0)
    return authenticated_get_seed, authenticated_main_password
