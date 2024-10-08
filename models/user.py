from sqlalchemy import Integer, String, Table, Column
from config.db import meta, engine
users = Table("users", meta, 
              Column("id", Integer, primary_key=True), 
              Column("name", String(40)),
              Column("email", String(40)),
              Column("password", String(40)))


meta.create_all(engine)