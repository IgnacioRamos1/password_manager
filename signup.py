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
    data = '{"data":{"user": "%s", "main_password": "%s", "seed_phrase": "%s"}}' % (user, main_password, seed)
    requests.post(url, headers=headers, data=data, verify=False)
    return seed

#porque debe tener 32 caracteres justo?

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
