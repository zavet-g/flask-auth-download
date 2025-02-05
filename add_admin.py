from sqlalchemy import create_engine, Column, Integer, String
import hashlib
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URI = 'sqlite:///instance/file_downloader.db'
engine = create_engine(DATABASE_URI, echo=True)

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

SessionLocal = sessionmaker(bind=engine)

def add_admin():
    login = input('Введите логин: ').strip()
    password = input('Введите пароль: ').strip()
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    session = SessionLocal()

    existing_user = session.query(Users).filter_by(login=login).first()
    if existing_user:
        print("Ошибка: Пользователь с таким логином уже существует.")
        session.close()
        return

    new_user = Users(login=login, password=hashed_password)
    session.add(new_user)

    try:
        session.commit()
        print("Администратор успешно добавлен!")
    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()

add_admin()
