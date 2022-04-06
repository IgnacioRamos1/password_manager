import click
from pymongo import MongoClient
from decrypt import decrypt

cluster = MongoClient(
    'mongodb+srv://IgnacioRamos:TZxa68aDGrWWVUeq@cluster0.tzlxj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    )
db = cluster['password_manager']
collection = db['accounts']


def search_username():
    username = click.prompt('Enter the username you wish to search')

    accounts = list(collection.find({'username': username}))

    if len(accounts) == 0:
        print("That username doesn't exist")
    else:
        for account in accounts:
            service = account['service']
            password = account['password']
            hashed_pasword = decrypt(password)

        print('----------------------')
        print(f'---- {service} ----')
        print(f'User  | {username}')
        print(f'Password | {hashed_pasword}')
