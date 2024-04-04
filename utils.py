from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],depricated = 'auto')

def Hash(password):
    return pwd_context.hash(password)
