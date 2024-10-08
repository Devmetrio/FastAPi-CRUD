from sqlalchemy import Integer, String, Table, Column
from config.db import meta, engine
users = Table("users", meta, 
              Column("id", Integer, primary_key=True, autoincrement=True), 
              Column("name", String(40)),
              Column("email", String(40)),
              Column("password", String(255)))


meta.create_all(engine)