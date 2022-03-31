import bcrypt


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
    print(pwd, hashed_pwd)
    if not isinstance(hashed_pwd, bytes):
        hashed_pwd = hashed_pwd.encode('utf_8')
    print(pwd, hashed_pwd)
    return bcrypt.checkpw(pwd, hashed_pwd)
