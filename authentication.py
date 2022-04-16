
import click
import requests
import uuid
from change_password import seed_phrase
requests.packages.urllib3.disable_warnings()


def url_headers():
    url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
    headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
    return url, headers


def change_main_password(seed):
    url, headers = url_headers()
    account = requests.get(url, headers=headers, verify=False)

    if account.json()['data']['data']['seed_phrase'] == seed:
        return True
    else:
        return False


def create_account(main_password):
    seed = seed_phrase()
    user = str(uuid.UUID(int=uuid.getnode()))
    data = '{"data":{"user": "%s", "main_password": "%s", "seed_phrase": "%s"}}' % (user, main_password, seed)
    url, headers = url_headers()
    requests.post(url, headers=headers, data=data, verify=False)
    return seed


def get_account(main_password):
    user = str(uuid.UUID(int=uuid.getnode()))
    url, headers = url_headers()
    account = requests.get(url, headers=headers, verify=False)

    return account.json()['data']['data']['user'] == user and account.json()['data']['data']['main_password'] == main_password


def user_exists():
    user = str(uuid.UUID(int=uuid.getnode()))
    url, headers = url_headers()
    account = requests.get(url, headers=headers, verify=False)

    return account.json()['data']['data']['user'] == user


def log_in():
    main_password = click.prompt(
        'Enter the main password to access',
        hide_input=True
        )

    return get_account(main_password)


def sign_up():
    main_password = click.prompt(
        'New password (must contain 32 characters)',
        hide_input=True
        )

    while len(main_password) != 32:
        main_password = click.prompt(
            'New passowrd (must contain 32 characters)',
            hide_input=True
            )

    main_password_2 = click.prompt('Confirm password', hide_input=True)

    if main_password == main_password_2:
        seed = create_account(main_password)
        return True, seed
    else:
        return False, None
