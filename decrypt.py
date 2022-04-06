import base64
from cryptography.fernet import Fernet

main_password = 'E2d25dSpas5NNHNE7fq5NCZSF6RTadtk'


def decrypt(password):
    key = base64.urlsafe_b64encode(main_password.encode('utf-8'))
    f = Fernet(key)
    plain_text_password = (f.decrypt(password)).decode('utf-8')
    return plain_text_password
