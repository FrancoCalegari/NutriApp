from typing import Union, Optional
from fastapi import FastAPI, HTTPException, Depends, Form
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Habilitar CORS para cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Simulación de base de datos (Se puede reemplazar mas adelante por sqlite3, mongodb, etc)
users_db = {}

# Contexto de cifrado para las contraseñas (Para proteccion de datos)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelos

#Se requiere usuario y contraseña aca
class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

# Utilidades
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user:
        return False
    if not verify_password(password, user['hashed_password']):
        return False
    return True

# Rutas

#Ruta principal

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

#Ruta de registro

@app.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Usuario ya registrado")
    hashed_password = get_password_hash(user.password)
    users_db[user.username] = {"username": user.username, "hashed_password": hashed_password}
    return {"msg": "Usuario registrado con éxito"}

#Ruta de Login

@app.post("/login")
def login(user: User):
    if authenticate_user(user.username, user.password):
        return {"msg": f"Bienvenido {user.username}"}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")



#Con el live server se puede testear