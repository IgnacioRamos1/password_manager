import requests
from seed_phrase_generator import seed_phrase
requests.packages.urllib3.disable_warnings()
import uuid

seed = seed_phrase()
data = '{"data":{"main_hashing_pw": "E2d25dSpas5NNHNE7fq5NCZSF6RTadtk"}}'
user = str(uuid.UUID(int=uuid.getnode()))
url = f'https://18.231.120.197:8200/v1/secret/data/password_manager'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
account = requests.get(url, headers=headers, verify=False)
requests.post(url, headers=headers, data=data, verify=False)

print(account.json()['data']['data']['seed_phrase'])
print(requests.get(url, headers=headers, data=data, verify=False).json())
