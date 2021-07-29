import re
from pydantic import BaseModel, EmailStr, validator


class CreateUserParams(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone: str = '1-111-111-1111'

    @validator('phone', pre=True)
    def valid_phone_number(cls, phone):
        pattern = r"^\d{1}.\d{3}.\d{3}.\d{4}$"
        valid = re.search(pattern, phone)
        if not valid:
            raise ValueError('Phone number is invalid! Use pattern [0-000-000-0000]')
        return phone


class User(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone: str
