
from PyInquirer import prompt
from examples import custom_style_2
from cryptography.fernet import Fernet
import base64
from pymongo import MongoClient
import random
import string
import click
import requests


cluster = MongoClient('mongodb+srv://IgnacioRamos:TZxa68aDGrWWVUeq@cluster0.tzlxj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster['password_manager']
collection = db['accounts']

main_password = 'E2d25dSpas5NNHNE7fq5NCZSF6RTadtk'


def sign_up():

    main_password = click.prompt(
        'New password (must contain 32 characters)'
        )

    while len(main_password) != 32:
        main_password = click.prompt(
            'Re-enter new passowrd (must contain 32 characters)'
            )

    main_password_2 = click.prompt('Confirm password')

    if main_password == main_password_2:
        url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
        headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
        info = '{"data":{"user": "%s"}}' % (main_password)

        r = requests.post(url, headers=headers, data=info, verify=False)

        print(r.json())
        print('The new password was set correctly')

        log_in()

    else:
        print("Passwords don't match")
        return 'error'


def log_in():
    # Ingresar main password para poder acceder al manager
    log_in_password = click.prompt(
        'Ingrese la main password para poder acceder'
        )

    url = 'https://18.231.120.197:8200/v1/secret/data/password_manager'
    headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
    r = requests.get(url, headers=headers, verify=False)
    print(r.json())
    if r.json()['data']['data']['user'] == log_in_password:
        print('Welcome!')
        menu()
    else:
        print('El usuario o la password es incorrecto')
        return 'error'


def menu():
    options = [
        'Seleccionar servicio',
        'Agregar cuenta nueva',
        'Generador de password',
        'Buscar un usuario',
        'Lista completa de cuentas',
        'Modificar una cuenta',
        'Eliminar una cuenta'
        ]
    questions = [
        {
            'type': 'list',
            'name': 'theme',
            'message': 'What do you want to do?',
            'choices': options
        }
    ]
    answers = prompt(questions, style=custom_style_2)
    if answers['theme'] == 'Seleccionar servicio':
        seleccionar_servicio()
    elif answers['theme'] == 'Agregar cuenta nueva':
        agregar_cuenta()
    elif answers['theme'] == 'Generador de password':
        random_pasword()
    elif answers['theme'] == 'Buscar un usuario':
        search_username()
    elif answers['theme'] == 'Lista completa de cuentas':
        complete_list()
    elif answers['theme'] == 'Modificar una cuenta':
        modify()
    elif answers['theme'] == 'Eliminar una cuenta':
        delete()

# ------------------------------------------------------


def seleccionar_servicio():
    busqueda = click.prompt(
        'Ingrese el servicio que desea buscar'
        ).capitalize()

    resultado = list(collection.find({'servicio': busqueda}))

    if len(resultado) == 0:
        # No existen cuentas para ese servicio
        print('No existen cuentas para ese servicio')
    else:
        for account in resultado:
            uhpassword = decrypt(account['password'])
            print('----------------------------')
            print(f'Usuario  | {account["username"]}')
            print(f'Passowrd | {uhpassword}')


def hashing(password):
    key = base64.urlsafe_b64encode(main_password.encode('utf-8'))
    f = Fernet(key)
    password = password.encode()
    hashed = f.encrypt(password)
    return hashed


def decrypt(password):
    key = base64.urlsafe_b64encode(main_password.encode('utf-8'))
    f = Fernet(key)
    unhashed = (f.decrypt(password)).decode('utf-8')
    return unhashed


def agregar_cuenta():
    servicio = click.prompt('Ingrese servicio').capitalize()

    username = click.prompt('Ingrese el usuario')

    check_1 = collection.find_one({'servicio': servicio, 'username': username})

    if check_1:
        if click.confirm('El usuario ya existe, desea cambiar la password?'):
            modify()
        else:
            menu()
    else:
        password = click.prompt('Ingrese la password')
        hashed = hashing(password)

        collection.insert_one(
            {
                'servicio': servicio,
                'username': username,
                'password': hashed
                }
                )


def random_pasword():
    length = click.prompt('Ingrese el largo de la password', type=int)
    print('Utilice y/n para marcar su eleccion')

    if click.confirm('Desea que contenga simbolos?'):
        # Con simbolos
        characters = list(string.ascii_letters + string.digits + '!@#$%^&*()')
        random.shuffle(characters)
        password = []
        for i in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        print(''.join(password))

    else:
        # Sin simbolos
        characters = list(string.ascii_letters + string.digits)
        random.shuffle(characters)
        password = []
        for i in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        print(''.join(password))


def search_username():
    username = click.prompt('Ingrese el usuario que desea buscar')

    accounts = list(collection.find({'username': username}))

    if len(accounts) == 0:
        print('No existe ese usuario')
    else:
        for account in accounts:
            servicio = account['servicio']
            password = account['password']
            uhpassword = decrypt(password)

        print('----------------------')
        print(f'---- {servicio} ----')
        print(f'Usuario  | {username}')
        print(f'Password | {uhpassword}')


def complete_list():
    total = collection.find({})
    for account in total:
        servicio = account['servicio']
        username = account['username']
        password = account['password']

        unhashed = decrypt(password)

        print('---------------------------')
        print(f'Servicio | {servicio}')
        print(f'Usuario  | {username}')
        print(f'Password | {unhashed}')


def modify():
    servicio = click.prompt(
        'Ingrese el servicio que desea modificar'
        ).capitalize()
    services = list(collection.find({'servicio': servicio}))

    if len(services) == 0:
        print(f'No se encuentra el servicio: {servicio} en la base de datos')
    else:
        options = [
                'Desea modificar el usuario?',
                'Desea modificar la password?'
                ]
        questions = [
                        {
                            'type': 'list',
                            'name': 'theme',
                            'message': 'What do you want to do?',
                            'choices': options
                        }
                    ]
        answers = prompt(questions, style=custom_style_2)
        
        if answers['theme'] == 'Desea modificar el usuario?':
            old_user = click.prompt('Ingrese el usuario que desea modificar')

            accounts = list(collection.find(
                {
                    'servicio': servicio,
                    'username': old_user
                }))

            if len(accounts) == 0:
                print(
                        f'No se encontro el usuario: {old_user} en el servicio: {servicio}'
                    )
            else:
                new_user = click.prompt('Ingrese el nuevo nombre de usuario')

                if click.confirm('Esta seguro que desea modificar el usuario?'):

                    collection.find_one_and_update(
                        {
                            'servicio': servicio,
                            'username': old_user
                        },
                        {
                            '$set': {'username': new_user}
                        })
                    print('El usuario se actualizo correctamente')

                else:
                    print('Se ha cancelado la operacion')

        elif answers['theme'] == 'Desea modificar la password?':
            user = click.prompt(
                'Ingrese el usuario que desea cambiarle la password'
                )
            check = list(collection.find(
                {
                    'servicio': servicio,
                    'username': user
                }))

            if len(check) == 0:
                print(f'No se encontro el usuario: {user} en el servicio: {servicio}')
            else:
                new_password = click.prompt('Ingrese la nueva password')

                if click.confirm('Esta seguro que desea modificar la password?'):
                    hashed = hashing(new_password)

                    collection.find_one_and_update(
                        {
                            'servicio': servicio,
                            'username': user
                        },
                        {
                            '$set': {'password': hashed}
                        })
                    print('La password se ha actualizado correctamente')

                else:
                    print('Se ha cancelado la operacion')

        else:
            print('La opcion ingresada no existe')


def delete():
    servicio = click.prompt('Ingrese el servicio que desea eliminar')

    services = list(collection.find({'servicio': servicio}))

    if len(services) == 0:
        print(f'No se encuentra el servicio: {servicio} en la base de datos')
    else:
        user = click.prompt('Ingrese el usuario que desea eliminar')
        accounts = list(collection.find(
            {
                'servicio': servicio,
                'username': user
            }))

        if len(accounts) == 0:
            print(f'No existe ningun usuario con el nombre: {user} en el servicio: {servicio}')

        else:
            if click.confirm('Se encontro la cuenta! \nEsta seguro que desea eliminarla?'):
                collection.find_one_and_delete(
                    {
                        'servicio': servicio,
                        'username': user
                    })
                print('Se ha eliminado la cuenta correctamente')
            else:
                print('Se ha cancelado la operacion')


# Si el tipo tiene ya una cuenta:
# log_in()
    # error = log_in()
    # if error = 'error':
        # lo mando de vuelta a la pagina principal
    # else:
    #   menu()

# Si no tiene una cuenta:
# sing_up()

    # error = sign_up()
    # if error = 'error':
        # lo mando de vuelta a la pagina principal
    # else:
    #   log_in()

menu()
