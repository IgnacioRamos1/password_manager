
import click
import requests
import uuid
from change_password import seed_phrase
requests.packages.urllib3.disable_warnings()

user = str(uuid.UUID(int=uuid.getnode()))
url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}


def user_exists():
    account = requests.get(url, headers=headers, verify=False)
    return account.json()['data']['data']['user'] == user


