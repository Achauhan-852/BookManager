from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends,UploadFile,File,HTTPException
from fastapi.responses import FileResponse
from app.db.config import create_tables, get_session
from app.account.services import *
from app.schemas.user import *
from app.auth_dependency import get_current_user
import os,shutil

UPLOAD_DIR = "uploads"
DOWNLOAD_DIR = "downloads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


# ===================== AUTH =====================

@app.post("/bm/signup", tags=["Login/Signup"])
async def signup(data: SignupPydantic, session: AsyncSession = Depends(get_session)):
    await sign_up_user(session, data.name, data.email, data.phone, data.password)
    return {"message": "Signup Successful", "email": data.email}


@app.post("/bm/login", tags=["Login/Signup"])
async def login(data: LoginPydantic, session: AsyncSession = Depends(get_session)):
    token = await login_user(session, data.email, data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"access_token": token, "token_type": "bearer"}


@app.get("/bm/me", tags=["Login/Signup"])
async def me(current_user=Depends(get_current_user)):
    return {"user_id": current_user.id, "email": current_user.email}


# ===================== CATEGORY =====================

@app.post("/bm/category", tags=["Category"])
async def add_category(data: CategoryPydantic, session: AsyncSession = Depends(get_session),current_user=Depends(get_current_user)):
    category = await create_category(session, data.cat_name)
    return {"message": "Category added", "category_id": category.id}


@app.get("/bm/list_category/", tags=["Category"])
async def get_category_list(session: AsyncSession = Depends(get_session),current_user=Depends(get_current_user)):
    return await get_all_category_list(session)


@app.get("/bm/category/{category_id}", tags=["Category"])
async def category_get_by_id(category_id: int, session: AsyncSession = Depends(get_session),current_user=Depends(get_current_user)):
    return await get_category_by_id(session, category_id)


@app.put("/bm/category/{category_id}", tags=["Category"])
async def update_category(category_id: int,data: CategoryUpdatePydantic,session: AsyncSession = Depends(get_session),current_user=Depends(get_current_user)):
    return await category_update(session, category_id, data.cat_name)


# ===================== AUTHOR =====================

@app.post("/bm/author", tags=["Author"])
async def add_author(data: AuthorPydantic, session: AsyncSession = Depends(get_session),current_user=Depends(get_current_user)):
    author = await create_author(session, data.name, data.age, data.country)
    return {"message": "Author added", "author_id": author.id}


@app.get("/bm/list_authors/", tags=["Author"])
async def get_authors_list(session: AsyncSession = Depends(get_session),current_user=Depends(get_current_user)):
    return await get_all_author_list(session)


@app.get("/bm/author/{author_id}", tags=["Author"])
async def author_get_by_id(author_id: int, session: AsyncSession = Depends(get_session),current_user=Depends(get_current_user)):
    return await get_author_by_id(session, author_id)


@app.put("/bm/author/{author_id}", tags=["Author"])
async def update_author(author_id: int,data: AuthorUpdatePydantic,session: AsyncSession = Depends(get_session),current_user=Depends(get_current_user)):
    return await author_update(session, author_id, data.name, data.age, data.country)


# ===================== BOOK (PROTECTED) =====================

@app.post("/bm/book", tags=["Book"])
async def add_book(data: BookPydantic,session: AsyncSession = Depends(get_session),current_user=Depends(get_current_user)):
    book, err = await create_book(
        session, data.title, data.author_id, data.category_id, data.amz_url
    )
    if err == "AUTHOR_NOT_FOUND":
        raise HTTPException(status_code=404, detail="Author not found")
    if err == "Category_NOT_Found":
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Book added", "book_id": book.id}


@app.get("/bm/list_book/", tags=["Book"])
async def get_book_list(session: AsyncSession = Depends(get_session),current_user=Depends(get_current_user)):
    return await get_all_book_list(session)


@app.get("/bm/book/{book_id}", tags=["Book"])
async def book_get_by_id(book_id: int,session: AsyncSession = Depends(get_session),current_user=Depends(get_current_user)):
    return await get_book_by_id(session, book_id)


@app.put("/bm/book/{book_id}", tags=["Book"])
async def update_book(book_id: int,data: BookUpdatePydantic,session: AsyncSession = Depends(get_session),current_user=Depends(get_current_user)):
    return await book_update(session, book_id, data.title, data.amz_url)

@app.post("/bm/upload", tags=["File Handling"])
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as upload:
        shutil.copyfileobj(file.file, upload)
    return {"message": "uploaded", "filename": file.filename}
@app.get("/bm/files", tags=["File Handling"])
async def list_files():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}
@app.get("/bm/download/{filename}", tags=["File Handling"])
async def download_file(filename: str):
    src = os.path.join(UPLOAD_DIR, filename)
    dst = os.path.join(DOWNLOAD_DIR, filename)
    print("SRC:", src)
    print("DST:", dst)
    if not os.path.exists(src):
        raise HTTPException(status_code=404, detail="File not found")
    shutil.copy(src, dst)
    print("COPIED OK")
    return FileResponse(dst, filename=filename)

