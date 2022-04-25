import click
import requests
import uuid
from seed_phrase_generator import seed_phrase
requests.packages.urllib3.disable_warnings()

user = str(uuid.UUID(int=uuid.getnode()))
url_main_password = f'https://18.231.120.197:8200/v1/secret/data/password_manager/user/{user}/main_password'
url_seed = f'https://18.231.120.197:8200/v1/secret/data/password_manager/user/{user}/seed'
url_user = f'https://18.231.120.197:8200/v1/secret/data/password_manager/user/{user}'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}


def create_account(main_password):
    seed = seed_phrase()
    data_main_password = '{"data": {"main_password": "%s"}}' % (main_password)
    data_seed = '{"data": {"seed_phrase": "%s"}}' % (seed)
    data_user = '{"data": {"user": "%s"}}' % (user)
    requests.post(url_main_password, headers=headers, data=data_main_password, verify=False)
    requests.post(url_seed, headers=headers, data=data_seed, verify=False)
    requests.post(url_user, headers=headers, data=data_user, verify=False)
    return seed


def sign_up():
    print('Welcome!, Please Sing Up.')
    main_password = click.prompt(
        'Enter new password',
        hide_input=True,
        confirmation_prompt=True
        )
    print('=========================================================================')
    print('Save this seed phrase, you will need it to reset your password')
    print('WARNING: This will be the last time you will see it')
    print('=========================================================================')
    print(create_account(main_password))
    print('=========================================================================')
