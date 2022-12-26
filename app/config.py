from pydantic import BaseSettings

# The below 2 lines of code should not be needed but without the load_dotenv() function the contents
# of .env file were not being read
from dotenv import load_dotenv
load_dotenv()

# Environment variables:
# This module takes the values from .env file so that they are stored as environment variables
# and not hard coded as python code. Especially useful when uploading code to github where multiple 
# people can see the sensitive info

class Settings(BaseSettings):
    database_name: str
    database_hostname: str
    database_username: str
    database_password: str 
    database_port: int
    secret_key: str 
    algorithm: str
    access_token_expire_minutes: int

    class config:
        env_file = ".env"

settings = Settings() # type: ignore