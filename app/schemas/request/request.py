from pydantic import BaseModel

# Define a Pydantic model for the login request
class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    email: str
    password: str