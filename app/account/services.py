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

async def create_author(session:AsyncSession,name:str,age:str,country:str):
    author = Author(name=name, age=age, country=country)
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

