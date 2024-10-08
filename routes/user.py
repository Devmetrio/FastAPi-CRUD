from fastapi import APIRouter, Response
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter() 
key = Fernet.generate_key()
f = Fernet(key)

@user.get('/user')
def get_Users():
    return conn.execute(users.select()).fetchall()

@user.post('/user')
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8")) 
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

@user.get('/user/{id}')
def get_user(id: str):
    return conn.execute(users.select().where(users.c.id == id)).first()


@user.delete('/user/{id}')
def delete_user():
    conn.execute(users.delete().where(users.c.id == id))
    return Response(status_code = HTTP_204_NO_CONTENT)
    
@user.put('/user/{id}')
def update_user(id:str , user: User):
    conn.execute(users.update().value(name = user.name, email = user.email, password = f.encrypt(user.password).encode("utf-8"))).where(users.c.id == id)
    return conn.execute(users.select().where(users.c.id == id)).first()
