import click
import requests
import uuid
from seed_phrase_generator import seed_phrase
requests.packages.urllib3.disable_warnings()

url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
user = str(uuid.UUID(int=uuid.getnode()))


def create_account(main_password):
    seed = seed_phrase()
    data = '{"data":{"user": "%s", "main_password": "%s", "seed_phrase": "%s", "main_hashing_pw": "E2d25dSpas5NNHNE7fq5NCZSF6RTadtk"}}' % (user, main_password, seed)
    requests.post(url, headers=headers, data=data, verify=False)
    return seed


def sign_up():
    main_password = click.prompt(
        'Enter new password',
        hide_input=True,
        confirmation_prompt=True
        )

    if main_password:
        seed = create_account(main_password)
        return True, seed
    else:
        return False, None
