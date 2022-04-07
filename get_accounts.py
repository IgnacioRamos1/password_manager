from decrypt import decrypt


def get_all_accounts(collection):
    accounts = collection.find({})
    for account in accounts:
        service = account['service']
        username = account['username']
        password = account['password']

        plain_text_password = decrypt(password)

        print('---------------------------')
        print(f'Servicio | {service}')
        print(f'Usuario  | {username}')
        print(f'Password | {plain_text_password}')
