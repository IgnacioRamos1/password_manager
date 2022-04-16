import requests
requests.packages.urllib3.disable_warnings()
from change_password import seed_phrase


seed = seed_phrase()
data = '{"data":{"user": "test", "main_password": "test", "seed_phrase": "%s"}}' % (seed)
url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
account = requests.get(url, headers=headers, verify=False)
requests.post(url, headers=headers, data=data, verify=False)

print(account.json()['data']['data']['seed_phrase'])

