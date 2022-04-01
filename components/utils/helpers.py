import bcrypt
from datetime import datetime


def encrypt_password(pwd):
    if not isinstance(pwd, bytes):
        pwd = pwd.encode('utf_8')
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
    hashed_str = hashed.decode('utf_8')
    return hashed_str


def check_password(pwd, hashed_pwd):
    print(pwd, hashed_pwd)
    if not isinstance(pwd, bytes):
        pwd = pwd.encode('utf_8')
    if not isinstance(hashed_pwd, bytes):
        hashed_pwd = hashed_pwd.encode('utf_8')
    return bcrypt.checkpw(pwd, hashed_pwd)


def datetime_validator(datetime_str):
    try:
        datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        return True
    except:
        return False


def string_to_datetime(str):
    try:
        return datetime.strptime(str, "%Y-%m-%d %H:%M")
    except:
        return str
