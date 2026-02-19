from pydantic import BaseModel,EmailStr
class SignupPydantic(BaseModel):
    name:str
    email:EmailStr
    phone:str
    password:str
class LoginPydantic(BaseModel):
    email:EmailStr
    password:str

class CategoryPydantic(BaseModel):
    cat_name:str

class AuthorPydantic(BaseModel):
    name:str
    age:int
    country:str

class BookPydantic(BaseModel):
    title: str
    author_id: int
    category_id: int
    amz_url: str | None = None
class CategoryUpdatePydantic(BaseModel):
    cat_name: str
class AuthorUpdatePydantic(BaseModel):
    name: str
    age:int
    country:str
class BookUpdatePydantic(BaseModel):
    title: str
    amz_url:int
