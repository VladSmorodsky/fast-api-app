from pydantic import BaseModel, EmailStr, field_validator, model_validator
import re


class TokenPayload(BaseModel):
    id: int


# Request body

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirmation: str

    @field_validator("password")
    def validate_password(cls, value):
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\d])(?=.*[@$!%*?&]).{8,}$', value) is None:
            raise ValueError(
                "Password must be 8 characters at least, and include at least one uppercase letter, one lowercase letter, one digit, and one special character (@$!%*?&).")
        return value

    @model_validator(mode='after')
    def validate_password_confirmation(self):
        if self.password != self.password_confirmation:
            raise ValueError('Passwords do not match.')
        return self


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Responses

class UserResponse(BaseModel):
    username: str
    email: str


class ResponseUserCreate(BaseModel):
    message: str
    user: UserResponse
    token: str


class ResponseUserLogin(BaseModel):
    user: UserResponse
    token: str
