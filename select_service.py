import click
from pymongo import MongoClient
from decrypt import decrypt

cluster = MongoClient(
    'mongodb+srv://IgnacioRamos:TZxa68aDGrWWVUeq@cluster0.tzlxj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    )
db = cluster['password_manager']
collection = db['accounts']


def select_service():
    search = click.prompt(
        'Enter the service you want to search'
        ).capitalize()
    print(search)
    result = list(collection.find({'service': search}))

    if len(result) == 0:
        # No existen cuentas para ese servicio
        print('There are not accounts for that service')
    else:
        for account in result:
            plain_text_password = decrypt(account['password'])
            print('----------------------------')
            print(f'User  | {account["username"]}')
            print(f'Password | {plain_text_password}')
