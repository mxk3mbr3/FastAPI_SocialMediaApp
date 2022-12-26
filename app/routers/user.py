from fastapi import HTTPException, APIRouter
from ..schemas import CreateUser, GetUser
from ..utils import hash
from .. import database
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/users", tags = ['Users'])

# Getting global variables con and cur
con = database.setup_connection()
cur = con.cursor(cursor_factory=RealDictCursor)

# Setting up user endpoints 

@router.post("/", status_code=201)
def create_user(user:CreateUser):
    # Hash the password - user.password
    hashed_pwd = hash(user.password)
    user.password = hashed_pwd
    # User inputting email and password 
    cur.execute("INSERT INTO users(email, password) VALUES (%s,%s) RETURNING *;", 
                (user.email,user.password))
    new_user = cur.fetchone() 
    # The below removes the password field from being shown back to user
    new_user.pop('password') # type:ignore
    # commit changes to database
    con.commit()
    return {"data":new_user}

@router.get("/")
def get_users():
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    users_cleaned = []
    for user in users:
        user.pop('password')
        users_cleaned.append(user)
    return {"data":users_cleaned}

@router.get("/{id}",response_model=GetUser)
def get_user(id:int):
    cur.execute(f"SELECT * FROM users WHERE id={id}")
    user_by_id = cur.fetchone()
    if user_by_id is None:
        raise HTTPException(status_code=404, 
                            detail = f"user with id {id} does not exist")
    return user_by_id