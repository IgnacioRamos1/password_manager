from pymongo import MongoClient
import click


cluster = MongoClient(
    'mongodb+srv://IgnacioRamos:TZxa68aDGrWWVUeq@cluster0.tzlxj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    )
db = cluster['password_manager']
collection = db['accounts']

def delete():
    service = click.prompt('Enter the service').capitalize()

    services = list(collection.find({'service': service}))

    if len(services) == 0:
        print(f'The service: {service} was not found in the data base')
    else:
        user = click.prompt('Enter the username you wish to delete')
        accounts = list(collection.find(
            {
                'service': service,
                'username': user
            }))

        if len(accounts) == 0:
            print(f'There is no username: {user} in the service: {service}')

        else:
            if click.confirm('The account was found! \nAre you sure you want to delete it?'):
                collection.find_one_and_delete(
                    {
                        'service': service,
                        'username': user
                    })
                print('The account was deleted correctly')
            else:
                print('The operation was cancelled')