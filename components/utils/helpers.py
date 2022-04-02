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


def date_validator(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False


def time_validator(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except:
        return False


def string_to_datetime(str):
    try:
        return datetime.strptime(str, "%Y-%m-%d %H:%M")
    except:
        return str


def schedule_date_validator(date):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    day_of_week = date_obj.isoweekday()
    if day_of_week == 7:
        return False
    return True


def start_time_validator(start):
    if start >= '09:00':
        return True
    return False


def end_time_validator(end):
    if end <= '17:00':
        return True
    return False
