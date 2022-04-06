from pymongo import MongoClient
from decrypt import decrypt

cluster = MongoClient(
    'mongodb+srv://IgnacioRamos:TZxa68aDGrWWVUeq@cluster0.tzlxj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    )
db = cluster['password_manager']
collection = db['accounts']


def get_all_accounts():
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