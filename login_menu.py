import login
from PyInquirer import prompt
from examples import custom_style_2
import change_main_pw
import authentication

def login_menu():
    options = [
        'Log in',
        'Change main password'
        ]
    questions = [
        {
            'type': 'list',
            'name': 'theme',
            'message': 'It seems you already have an account',
            'choices': options
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    if answers['theme'] == 'Log in':
        login()
    elif answers['theme'] == 'Change main password':
        change_main_pw()