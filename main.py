from login_menu import login_menu
from login import log_in
from signup import sign_up
from authentication import user_exists


def password_manager():
    if user_exists():
        login_menu()
    else:
        sign_up()
        log_in()


if __name__ == "__main__":
    password_manager()
