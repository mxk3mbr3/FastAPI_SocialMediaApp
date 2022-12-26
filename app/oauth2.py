from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schemas, database
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from psycopg2.extras import RealDictCursor
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Getting global variables con and cur
con = database.setup_connection()
cur = con.cursor(cursor_factory=RealDictCursor)

# Secret key can be generated, this was copied straight from FastAPI documentation
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

# Expiration time - how long you're logged in. 
# Setting user to be only logged in with a specific token for X no. of minutes
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Creates access token
def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

# Verifies access token by decoding the access token to check if credentials match. 
# This is done by extracting the id from JWT token
def verify_access_token(token:str, credentials_exception):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get("user_id") # Extract id from JWT token - "user_id" is found in auth.py access token

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id) # Validating schema. Note that int his case token_data is only the id
    
    except JWTError:
        raise credentials_exception
    
    return token_data

# Takes token from one of the path operations (end points) and verifies token is correct by using the above function
def get_current_user(token:str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(status_code=401, detail = "Could not validate credentials", 
                                            headers= {"WWW-Authenticate":"Bearer"})

    token_data = verify_access_token(token, credentials_exception)

    cur.execute("SELECT * FROM users WHERE id = (%s)",(token_data.id,))
    user = cur.fetchone()

    return user