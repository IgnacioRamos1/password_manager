
import requests
import uuid
import click
requests.packages.urllib3.disable_warnings()

user = str(uuid.UUID(int=uuid.getnode()))
url_seed = f'https://18.231.120.197:8200/v1/secret/data/password_manager/user/{user}/seed'
url_main_password = f'https://18.231.120.197:8200/v1/secret/data/password_manager/user/{user}/main_password'
headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}


def post_main_password():
    main_password = click.prompt(
        'Enter new password',
        hide_input=True,
        confirmation_prompt=True
    )
    data_main_password = '{"data": {"main_password": "%s"}}' % (main_password)
    requests.post(url_main_password, headers=headers, data=data_main_password, verify=False)


def change_mainpw():
    vault_stored_seed = requests.get(url_seed, headers=headers, verify=False).json()['data']['data']['seed_phrase']

    for attempt in range(3):
        seed_input = click.prompt('Enter the 12 words with spaces in between them')

        if attempt == 3:
            print('Too many wrong attempts')
            exit()
        elif seed_input != vault_stored_seed:
            continue

        else:
            post_main_password()
            exit()
