from app.db.config import Base
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "table_user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

class Login(Base):
    __tablename__ = "table_login"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id:Mapped[int]=mapped_column(Integer,ForeignKey("table_user.id"))

class Category(Base):
    __tablename__ = "table_category"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    cat_name:Mapped[str]=mapped_column(String(120),nullable=False)

class Author(Base):
     __tablename__ = "table_author"
     id: Mapped[int] = mapped_column(Integer, primary_key=True)
     name:Mapped[str]=mapped_column(String(120),nullable=False)
     age: Mapped[int] = mapped_column(Integer)
     country: Mapped[str] = mapped_column(String(120))

class Book(Base):
     __tablename__ = "table_books"
     id: Mapped[int] = mapped_column(Integer, primary_key=True)
     title:Mapped[str]=mapped_column(String(200),nullable=False)
     author_id: Mapped[str] = mapped_column(Integer,ForeignKey("table_author.id"))
     category_id: Mapped[str] = mapped_column(Integer, ForeignKey("table_category.id"))
     amz_url: Mapped[str] = mapped_column(String(255))



