import click
from PyInquirer import prompt
from examples import custom_style_2


def modify(collection):
    service = click.prompt(
         'Enter the service'
         ).capitalize()
    services = list(collection.find({'service': service}))

    if len(services) == 0:
        print(f'The service: {service} is not found in the data base')
    else:
        options = [
            'User',
            'Password'
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

        if answers['theme'] == 'User':
            old_user = click.prompt('Enter the username of the account')
            accounts = list(collection.find(
                {
                    'service': service,
                    'username': old_user
                }))

            if len(accounts) == 0:
                print(
                        f'The user: {old_user} was not found in the service: {service}'
                    )
            else:
                new_user = click.prompt('Enter the new username')

                if click.confirm(f'\nAre you sure you want to modify the user?\n{old_user} --> {new_user}'):

                    collection.find_one_and_update(
                        {
                            'service': service,
                            'username': old_user
                        },
                        {
                            '$set': {'username': new_user}
                        })
                    print('The username was updated correctly')

                else:
                    print('The operation was cancelled')

        elif answers['theme'] == 'Password':
            old_user = click.prompt('Enter the username of the account')
            account = list(collection.find(
                {
                    'service': service,
                    'username': old_user
                }))

            if len(account) == 0:
                print(f'The user: {old_user} was not found in the service: {service}')
            else:
                new_password = click.prompt(
                        'Enter the new password',
                        confirmation_prompt=True,
                        hide_input=True
                        )

                if click.confirm('Are you sure you want to modify the password?'):
                    hashed_pasword = hashing(new_password)

                    collection.find_one_and_update(
                        {
                            'service': service,
                            'username': old_user
                        },
                        {
                            '$set': {'password': hashed_pasword}
                        })
                    print('The password was updated correctly')

                else:
                    print('The operation was cancelled')
