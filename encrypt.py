import base64
from cryptography.fernet import Fernet

main_password = 'E2d25dSpas5NNHNE7fq5NCZSF6RTadtk'


def hashing(password):
    key = base64.urlsafe_b64encode(main_password.encode('utf-8'))
    f = Fernet(key)
    hashed_pasword = f.encrypt(password.encode())
    return hashed_pasword
