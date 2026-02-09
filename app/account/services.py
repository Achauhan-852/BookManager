from fastapi import HTTPException
from app.account.models import User,Login,Category,Author,Book
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def sign_up_user(session:AsyncSession,name:str,email:str,phone:str,password:str):
    user=User(name=name,email=email,phone=phone,password=password)
    session.add(user)
    await  session.commit()
    await session.refresh(user)
    return user
async def login_user(session:AsyncSession,email:str,password:str):
    result=await session.execute(select(User).where(User.email==email,User.password==password))
    user=result.scalar_one_or_none()
    if not user:
        return None
    login_data=Login(user_id=user.id)
    session.add(login_data)
    await session.commit()
    return user


async def create_category(session:AsyncSession,cat_name:str):
    category=Category(cat_name=cat_name)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category
async def get_all_category_list(session:AsyncSession):
    stmt=select(Category)
    result=await session.execute(stmt)
    categories=result.scalars().all()
    return categories
async def get_category_by_id(session:AsyncSession,id:int):
    result=await session.get(Category,id)
    if not result:
        raise HTTPException(status_code=1001,detail="Category not found")
    return result
async def category_update(session:AsyncSession,id:int,cat_name:str):
    category=await session.get(Category,id)
    if not category:
        raise HTTPException(status_code=602,detail="Category not found for update")
    category.cat_name=cat_name
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def create_author(session:AsyncSession,name:str,age:int,country:str):
    author = Author(name=name, age=age, country=country)
    session.add(author)
    await session.commit()
    await session.refresh(author)
    return author
async def get_all_author_list(session:AsyncSession):
    stmt=select(Author)
    result=await session.execute(stmt)
    authors=result.scalars().all()
    return authors
async def get_author_by_id(session:AsyncSession,id:int):
    result=await session.get(Author,id)
    if not result:
        raise HTTPException(status_code=1001,detail="Author not found")
    return result
async def author_update(session:AsyncSession,id:int,name:str,age:int,country:str):
    author=session.get(Author,id)
    if not author:
        raise HTTPException(status_code=602,detail="Author not found for update")
    author.name=name
    author.age=age
    author.country=country
    session.add(author)
    await session.commit()
    await session.refresh(author)
    return author


async def create_book(session:AsyncSession,title:str,author_id:int,category_id:int,amz_url:str | None=None):
    author=await session.get(Author,author_id)
    if not author:
        return None,"AUTHOR_NOT_FOUND"
    category=await session.get(Category,category_id)
    if not category:
        return None,"Category_NOT_Found"
    book=Book(title=title,author_id=author_id,category_id=category_id,amz_url=amz_url)
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book, None
async def get_all_book_list(session:AsyncSession):
    stmt=select(Book)
    result=await session.execute(stmt)
    book=result.scalars().all()
    return book
async def get_book_by_id(session:AsyncSession,id:int):
    result=await session.get(Book,id)
    if not result:
        raise HTTPException(status_code=1001,detail="Book not found")
    return result
async def book_update(session:AsyncSession,id:int,title:str,amz_url:str):
    book=await session.get(Book,id)
    if not book:
        raise HTTPException(status_code=602,detail="Book not found for update")
    book.title=title
    book.amz_url = amz_url
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book
