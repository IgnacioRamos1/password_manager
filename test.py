'''data = {'data':{'data': {'hola': '12345678910121314151617181920212'}}}

for key in data['data']['data'].keys():
    print(key)

test = input('enter: ')

if test == key:
    print('son iguales')
else:
    print('no son iguales')'''
import requests
import uuid

url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
r = requests.get(url, headers=headers, verify=False)

print(r.json())

for key in r.json()['data']['data'].keys():
    stored_user = key

print(type(stored_user))
print(stored_user)

user = str(uuid.UUID(int=uuid.getnode()))
print(user)
print(type(user))