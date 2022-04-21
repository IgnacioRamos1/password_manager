
import requests
import uuid

requests.packages.urllib3.disable_warnings()

user = str(uuid.UUID(int=uuid.getnode()))
url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}


def user_exists():
    account = requests.get(url, headers=headers, verify=False)
    return account.json()['data']['data']['user'] == user


def confirmation(function, value):
    funcion, seed = function()
    if funcion:
        return True, seed
    elif value >= 2:
        return False, None
    else:
        return confirmation(function, value+1)
