import base64
from cryptography.fernet import Fernet
import requests
import uuid

url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
user = str(uuid.UUID(int=uuid.getnode()))


def get_main_password():
    account = requests.get(url, headers=headers, verify=False)
    return account.json()['data']['data']['main_hashing_pw']


main_password = get_main_password()


def decrypt(password):
    key = base64.urlsafe_b64encode(main_password.encode('utf-8'))
    f = Fernet(key)
    plain_text_password = (f.decrypt(password)).decode('utf-8')
    return plain_text_password
