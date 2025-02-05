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
session = SessionLocal()

def del_admin():
    login = input('Введите логин: ').strip()
    password = input('Введите пароль: ').strip()
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    user_to_delete = session.query(Users).filter_by(login=login, password=hashed_password).first()

    if user_to_delete:
        try:
            session.delete(user_to_delete)
            session.commit()
            print("Администратор успешно удален!")
        except Exception as e:
            session.rollback()
            print(f"Ошибка: {e}")
    else:
        print("Пользователь с таким логином и паролем не найден.")

    session.close()

del_admin()
