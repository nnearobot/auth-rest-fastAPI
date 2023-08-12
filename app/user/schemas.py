from pydantic import BaseModel

class UserRead(BaseModel):
    id: int
    user_id: str
    nickname: str
    comment: str
    password_hash: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    user_id: str
    password: str