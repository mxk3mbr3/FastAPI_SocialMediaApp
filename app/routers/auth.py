from fastapi import APIRouter, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from .. import schemas, database, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags = ['Authentication'])

# Getting global variables con and cur
con = database.setup_connection()
cur = con.cursor(cursor_factory=RealDictCursor)

# Below function gives the user the JWT token upon inputting correct email and password to access their account
# This token will then be validated by the API

@router.get('/login', response_model=schemas.Token)

def login(user_credentials:OAuth2PasswordRequestForm = Depends()):
    # username here below is the default name as per OAuth2PasswordRequestForm. In our case this represents the email
    # This is only done so in Postman you can use the form-data under Body
    cur.execute("SELECT * FROM users WHERE email= (%s);",(user_credentials.username,)) # %s needs to be replaced by a tuple
    details = cur.fetchone()
    id = details['id'] #type:ignore
    email = details['email'] #type:ignore
    password = details['password'] #type:ignore

    if email is None:
        raise HTTPException(status_code=403, 
                            detail = f"Invalid Credentials")
    
    # Check if password inputted by user (which will be hashed) == to hashed password stored in db
    if not utils.verify_password(user_credentials.password,password):
        raise HTTPException(status_code=403,
                            detail = f"Invalid Credentials")

    # Creating and returning a token
    access_token = oauth2.create_access_token(data = {"user_id":id}) #type:ignore
    
    # The standard is for token type to be "bearer"
    return {"access_token": access_token, "token_type":"bearer"}