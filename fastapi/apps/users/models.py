import re
from pydantic import BaseModel, EmailStr, validator


class CreateUserParams(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone: str


class User(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone: str

    @validator('phone', pre=True)
    def valid_phone_number(cls, phone):
        pattern = r'^[0-9]{10}'
        valid = re.search(pattern, phone)
        if not valid:
            raise ValueError('Phone number is invalid! Use pattern [0123456789]')
