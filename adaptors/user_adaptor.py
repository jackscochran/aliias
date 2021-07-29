from passlib.hash import sha256_crypt
from data.users import User

# ----------- User Functions ----------- #

def add_user(email, password):
    user = User()
    user.password_hash = sha256_crypt.encrypt(password)
    user.email = email
    user.save()

def check_credentials(email, password):
    user = get_user(email)

    is_valid = sha256_crypt.verify(password, user.password_hash)

    return is_valid

def get_user(email):
    return User.objects(email=email).first()