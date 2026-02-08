print(" THIS MAIN.PY IS LOADED ")
from contextlib import asynccontextmanager
from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel,EmailStr
from app.db.config import create_tables,get_session
from app.account.services import sign_up_user,login_user,create_category,create_author,create_book
from sqlalchemy.ext.asyncio import AsyncSession
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)
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


@app.post("/bm/signup")
async def signup(data:SignupPydantic,session:AsyncSession=Depends(get_session)):
    user=await sign_up_user(session,data.name,data.email,data.phone,data.password)
    return {"message":"Signup Successful","User__id":user.id}

@app.post("/bm/login")
async def login(data:LoginPydantic,session:AsyncSession=Depends(get_session)):
    user=await login_user(session,data.email,data.password)
    if not user:
        raise HTTPException(status_code=450,detail="Invalid email or password")
    return {"message":"Login Successful","user_id":user.id}

@app.post("/bm/category")
async def add_category(data:CategoryPydantic,session:AsyncSession=Depends(get_session)):
    category=await create_category(session,data.cat_name)
    return {"message":"Category added","category_id":category.id}

@app.post("/bm/author")
async def add_author(data:AuthorPydantic,session:AsyncSession=Depends(get_session)):
    author=await create_author(session,data.name,data.age,data.country)
    return {"message":"Category added","author_id":author.id}

@app.post("/bm/book")
async def add_book(data:BookPydantic,session:AsyncSession=Depends(get_session)):
    book,err=await create_book(session,data.title,data.author_id,data.category_id,data.amz_url)
    if err=="AUTHOR_NOT_FOUND":
        raise HTTPException(status_code=452,detail="AUTHOR_NOT_FOUND")
    if err=="Category_NOT_Found":
        raise HTTPException(status_code=452,detail="Category_NOT_Found")
    return {"message":"Book added","book_id":book.id}
print("END OF FILE ")
