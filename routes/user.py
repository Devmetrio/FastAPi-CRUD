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
    try:
        new_user = {"name": user.name, "email": user.email}
        new_user["password"] = f.encrypt(user.password.encode("utf-8"))
        result = conn.execute(users.insert().values(new_user))
        conn.commit()

        # Obtener el ID del usuario insertado
        last_inserted_id = result.lastrowid
        # Consultar el usuario recién insertado y convertirlo a un diccionario
        inserted_user = conn.execute(users.select().where(users.c.id == last_inserted_id)).first()
        # Convertir el resultado a un diccionario antes de devolverlo
        inserted_user_dict = dict(inserted_user._asdict())
        return inserted_user_dict
    
    except SQLAlchemyError as e:
        print(str(e))
        return {"error": str(e)}

@user.get('/user/{id}')
def get_user(id: str):
    return conn.execute(users.select().where(users.c.id == id)).first()


@user.delete('/user/{id}')
def delete_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    return Response(status_code = HTTP_204_NO_CONTENT)
    
@user.put('/user/{id}')
def update_user(id:str , user: User):
    conn.execute(users.update().where(users.c.id == id).values(
        name=user.name,
        email=user.email,
        password=f.encrypt(user.password.encode("utf-8"))
    ))
    return conn.execute(users.select().where(users.c.id == id)).first()
