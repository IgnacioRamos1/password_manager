from login import log_in
from PyInquirer import prompt
from examples import custom_style_2
from change_main_pw import change_mainpw


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
        log_in()
    elif answers['theme'] == 'Change main password':
        change_mainpw()
        log_in()
