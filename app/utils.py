from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hash function is used so that the password given by the user when creating account is stored hashed in the database

def hash(password:str):
    return pwd_context.hash(password)

# verify_password function is used when user attempt to login account to check whether the password is correct
# You get the inputted password (plan password) which is compared against the stored hashed password in database

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)