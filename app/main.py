from datetime import datetime, timedelta,timezone
print(" THIS MAIN.PY IS LOADED ")
from contextlib import asynccontextmanager
from fastapi import FastAPI,Depends,Request,Response,middleware
from app.db.config import create_tables,get_session
from app.account.services import *
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import *
from app.auth_dependency import get_current_user
from app.auth_utils import decode_access_token

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Access Denied: Token Missing")
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")
    try:
        payload = decode_access_token(token)
    except:
        raise HTTPException(status_code=401, detail="Access Denied: Invalid Token")
    exp_ts = payload.get("exp")
    exp_time = datetime.fromtimestamp(exp_ts, tz=timezone.utc)
    if datetime.now(timezone.utc) > exp_time:
        raise HTTPException(status_code=401, detail="Access Denied: Token Expired")
    if datetime.now(timezone.utc) > exp_time + timedelta(seconds=30):
        raise HTTPException(status_code=401, detail="Access Denied: Token Grace Expired")
    return await call_next(request)

@app.post("/bm/signup",tags=["Login/Signup"])
async def signup(data:SignupPydantic,session:AsyncSession=Depends(get_session)):
    await sign_up_user(session,data.name,data.email,data.phone,data.password)
    return {"message":"Signup Successful","User__email":data.email}
@app.post("/bm/login",tags=["Login/Signup"])
async def login(data:LoginPydantic,session:AsyncSession=Depends(get_session)):
    token = await login_user(session,data.email,data.password)
    if not token:
        raise HTTPException(status_code=401,detail="Invalid email or password")
    return {
        "access_token": token,
        "token_type": "bearer"
    }
@app.get("/bm/me")
async def me(current_user = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "email": current_user.email
    }



@app.post("/bm/category",tags=["Category"])
async def add_category(data:CategoryPydantic,session:AsyncSession=Depends(get_session)):
    category=await create_category(session,data.cat_name)
    return {"message":"Category added","category_id":category.id}
@app.get("/bm/list_category/",tags=["Category"])
async def get_category_list(session:AsyncSession=Depends(get_session)):
    list_cat=await get_all_category_list(session)
    return list_cat
@app.get("/bm/{category_id}",tags=["Category"])
async def category_get_by_id(category_id:int,session:AsyncSession=Depends(get_session)):
    category =await get_category_by_id(session,category_id)
    return category
@app.put("/bm/category/{category_id}", tags=["Category"])
async def update_category(category_id: int,data: CategoryUpdatePydantic,session: AsyncSession = Depends(get_session)):
     category=await category_update(session, category_id, data.cat_name)
     return category

@app.post("/bm/author",tags=["Author"])
async def add_author(data:AuthorPydantic,session:AsyncSession=Depends(get_session)):
    author=await create_author(session,data.name,data.age,data.country)
    return {"message":"Category added","author_id":author.id}
@app.get("/bm/list_authors/",tags=["Author"])
async def get_authors_list(session:AsyncSession=Depends(get_session)):
    list_aut=await get_all_author_list(session)
    return list_aut
@app.post("/bm/{author_id}",tags=["Author"])
async def category_get_by_id(author_id:int,session:AsyncSession=Depends(get_session)):
    category =await get_category_by_id(session,author_id)
    return category
@app.post("/bm/{author_id}",tags=["Author"])
async def author_get_by_id(author_id:int,session:AsyncSession=Depends(get_session)):
    author =await get_author_by_id(session,author_id)
    return author
@app.put("/bm/author/{author_id}", tags=["Author"])
async def update_author(author_id: int,data: AuthorUpdatePydantic,session: AsyncSession = Depends(get_session)):
     author=await author_update(session, author_id, data.name,data.age,data.country)
     return author

@app.post("/bm/book",tags=["Book"])
async def add_book(data:BookPydantic,session:AsyncSession=Depends(get_session)):
    book,err=await create_book(session,data.title,data.author_id,data.category_id,data.amz_url)
    if err=="AUTHOR_NOT_FOUND":
        raise HTTPException(status_code=452,detail="AUTHOR_NOT_FOUND")
    if err=="Category_NOT_Found":
        raise HTTPException(status_code=452,detail="Category_NOT_Found")
    return {"message":"Book added","book_id":book.id}
@app.get("/bm/list_book/",tags=["Book"])
async def get_book_list(session:AsyncSession=Depends(get_session)):
    list_book = await get_all_book_list(session)
    return list_book
@app.post("/bm/{book_id}",tags=["Book"])
async def book_get_by_id(book_id:int,session:AsyncSession=Depends(get_session)):
    book =await get_book_by_id(session,book_id)
    return book
@app.put("/bm/book/{book_id}", tags=["Book"])
async def update_book(book_id: int,data: BookUpdatePydantic,session: AsyncSession = Depends(get_session)):
     book=await book_update(session, book_id, data.title,data.amz_url)
     return book

print("END OF FILE ")

