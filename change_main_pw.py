
import requests
import uuid
requests.packages.urllib3.disable_warnings()

url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
user = str(uuid.UUID(int=uuid.getnode()))


def check_seed(seed):
    account = requests.get(url, headers=headers, verify=False)

    if account.json()['data']['data']['seed_phrase'] == seed:
        return True
    else:
        return False
