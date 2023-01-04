from fastapi import FastAPI
from .routers import post, user, auth, vote
from . import database
from fastapi.middleware.cors import CORSMiddleware

# Making app variable an instance of the class FastAPI 
app = FastAPI()

# Using * wildcard in origins will allow every single domain/origin to make cross-origin requests 
# Note: If you only wanted certain domains to make these requests you would do as follows:  
# origins = ["https://www.google.com","https://www.youtube.com"]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initializing con and cur 
con = None
cur = None

try:
    # Getting posts & users tables
    database.table_setup()
 
    # Setting up 1st CRUD endpoint 
    @app.get("/")
    def root():
        return {"message":"Welcome to your favourite Social Media app"}

    # Linking app instance to router variable for post, user and auth python 
    # The below contain almost all the endpoints for the API
    app.include_router(post.router)
    app.include_router(user.router)
    app.include_router(auth.router)
    app.include_router(vote.router)

except Exception as error:
    print("Could not connect to database")
    print("Error:", error)