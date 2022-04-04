
from PyInquirer import prompt
from examples import custom_style_2
from cryptography.fernet import Fernet
import base64
from pymongo import MongoClient
import random
import string
import hvac
import click
import requests

HOLA LO CAMBIE AL ARCHkjgjhkgjhvj

cluster = MongoClient('mongodb+srv://IgnacioRamos:TZxa68aDGrWWVUeq@cluster0.tzlxj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster['password_manager']
collection = db['accounts']

mainpw = 'E2d25dSpas5NNHNE7fq5NCZSF6RTadtk'


def sign_up():
    mainpw = click.prompt('Ingrese la nueva password (debe tener 32 caracteres)')

    while len(mainpw) != 32:
        mainpw = click.prompt('Ingrese la nueva password (debe tener 32 caracteres)')

    mainpw_2 = click.prompt('Ingrese nuevamente la password')

    if mainpw == mainpw_2:
        url ='https://18.231.120.197:8200/v1/secret/data/password_manager'
        headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
        r = requests.post(url, headers=headers, data={'user': mainpw}, verify=False)
        print('La password fue seteada correctamente')

        log_in()

    else:
        print('Las password no coinciden')
        sign_up()


def log_in():
    # ingresar main password para poder acceder al manager
    try_1 = click.prompt('Ingrese la main password para poder acceder')

    url ='https://18.231.120.197:8200/v1/secret/data/password_manager'
    headers = {'X-Vault-Token': 'hvs.2mYiopcfyjBbvdbiMFmaxt9H'}
    r = requests.get(url, headers=headers, verify=False)

    if r.json()['data']['data']['user'] == try_1:
        print('Welcome!')
        menu()
    else:
        print('El usuario o la password es incorrecto')
        log_in()


def menu():
    options = ['Seleccionar servicio', 'Agregar cuenta nueva', 'Generador de password', 'Buscar un usuario', 'Lista completa de cuentas', 'Modificar una cuenta', 'Eliminar una cuenta']
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
    busqueda = click.prompt('Ingrese el servicio que desea buscar').capitalize()

    resultado = list(collection.find({'servicio': busqueda}))

    if len(resultado) == 0:
        # no existen cuentas para ese servicio
        print('No existen cuentas para ese servicio')
    else:
        for account in resultado:
            uhpassword = decrypt(account['password'])
            print('----------------------------')
            print(f'Usuario  | {account["username"]}')
            print(f'Passowrd | {uhpassword}')


def hashing(password):
    key = base64.urlsafe_b64encode(mainpw.encode('utf-8'))
    f = Fernet(key)
    password = password.encode()
    hashed = f.encrypt(password)
    return hashed


def decrypt(password):
    key = base64.urlsafe_b64encode(mainpw.encode('utf-8'))
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

        collection.insert_one({'servicio': servicio, 'username': username, 'password': hashed})


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
    servicio = click.prompt('Ingrese el servicio que desea modificar').capitalize()
    services = list(collection.find({'servicio': servicio}))

    if len(services)== 0:
        print(f'No se encuentra el servicio: {servicio} en la base de datos')
    else:
        eleccion = click.prompt('1. Desea modificar el usuario? \n2. Desea modificar la password? \nEleccion', type=int)
        if eleccion == 1:
            old_user = click.prompt('Ingrese el usuario que desea modificar')

            accounts = list(collection.find({'servicio':servicio, 'username':old_user}))

            if len(accounts) == 0:
                print(f'No se encontro el usuario: {old_user} en el servicio: {servicio}')
            else:
                new_user = click.prompt('Ingrese el nuevo nombre de usuario')

                if click.confirm('Esta seguro que desea modificar el usuario?'):

                    collection.find_one_and_update({'servicio': servicio, 'username': old_user}, {'$set': {'username': new_user}})
                    print('El usuario se actualizo correctamente')

                else:
                    print('Se ha cancelado la operacion')

        elif eleccion == 2:
            user = click.prompt('Ingrese el usuario que desea cambiarle la password')
            check = list(collection.find({'servicio': servicio, 'username': user}))

            if len(check) == 0:
                print(f'No se encontro el usuario: {user} en el servicio: {servicio}')
            else:
                new_password = click.prompt('Ingrese la nueva password')

                if click.confirm('Esta seguro que desea modificar la password?'):
                    hashed = hashing(new_password)

                    collection.find_one_and_update({'servicio': servicio, 'username': user}, {'$set': {'password': hashed}})
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
        accounts = list(collection.find({'servicio': servicio, 'username': user}))

        if len(accounts) == 0:
            print(f'No existe ningun usuario con el nombre: {user} en el servicio: {servicio}')

        else:
            if click.confirm('Se encontro la cuenta! \nEsta seguro que desea eliminarla?'):
                collection.find_one_and_delete({'servicio': servicio, 'username': user})
                print('Se ha eliminado la cuenta correctamente')
            else:
                print('Se ha cancelado la operacion')

#menu()
sign_up()
