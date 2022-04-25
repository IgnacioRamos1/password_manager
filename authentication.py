
import requests
import uuid

requests.packages.urllib3.disable_warnings()

user = str(uuid.UUID(int=uuid.getnode()))
url = f'https://18.231.120.197:8200/v1/secret/data/password_manager/user/{user}'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}


def user_exists():
    account = requests.get(url, headers=headers, verify=False)
    print(account.status_code)
    return account.status_code != 404

