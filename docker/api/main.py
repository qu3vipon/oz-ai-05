from fastapi import FastAPI
from sqlalchemy import text

from connection import SessionFactory


app = FastAPI()

@app.get("/hello")
def hello():
    return {"msg": "hello"}

@app.get("/users")
def get_users_handler():
    with SessionFactory() as session:
        stmt = text("SELECT * FROM user;")
        rows = session.execute(stmt)
        users = [row._asdict() for row in rows]
    return {"users": users}
