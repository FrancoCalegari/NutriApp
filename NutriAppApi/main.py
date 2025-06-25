from typing import Union, Optional
from fastapi import FastAPI, HTTPException,Body
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
import sqlite3


app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a la base de datos
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_users_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            profile_picture TEXT,
            full_name TEXT,
            height REAL DEFAULT 0,
            weight REAL DEFAULT 0,
            total_calories INTEGER DEFAULT 0,
            hashed_password TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


# LLAMADA INMEDIATA
create_users_table()


# Contexto de cifrado
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelos
class User(BaseModel):
    username: str
    password: str

class UserRegister(User):
    email: Optional[str] = None
    profile_picture: Optional[str] = None

class UserResponse(BaseModel):
    username: str
    email: Optional[str]
    profile_picture: Optional[str]
    full_name: Optional[str]
    height: Optional[float]
    weight: float
    total_calories: int



# Funciones auxiliares
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(username: str, hashed_password: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return True

# Rutas

@app.get("/")
def read_root():
    return {"NutriAPP": "V01"}

@app.post("/register")
def register(user: UserRegister):
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Usuario ya registrado")
    
    hashed_password = get_password_hash(user.password)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, email, profile_picture, hashed_password)
        VALUES (?, ?, ?, ?)
    """, (user.username, user.email, user.profile_picture, hashed_password))
    conn.commit()
    conn.close()
    
    user_id = cursor.lastrowid
    return {"msg": "Usuario registrado con éxito", "id": user_id}



@app.post("/login", response_model=UserResponse)
def login(user: User):
    db_user = get_user(user.username)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    return {
        "id": db_user["id"],
        "username": db_user["username"],
        "email": db_user["email"],
        "profile_picture": db_user["profile_picture"],
        "full_name": db_user["full_name"],
        "height": db_user["height"],
        "weight": db_user["weight"],
        "total_calories": db_user["total_calories"],
    }


@app.post("/update_user")
def update_user(data: dict):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE users
            SET weight = ?, total_calories = ?
            WHERE username = ?
        """, (data["weight"], data["total_calories"], data["username"]))
        conn.commit()
        return {"msg": "Datos actualizados con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.post("/update_profile")
def update_profile(data: dict = Body(...)):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE users
            SET email = ?, profile_picture = ?, weight = ?, total_calories = ?
            WHERE username = ?
        """, (
            data.get("email"),
            data.get("profile_picture"),
            data.get("weight"),
            data.get("total_calories"),
            data.get("username")
        ))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"msg": "Perfil actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "username": user["username"],
        "email": user["email"],
        "profile_picture": user["profile_picture"],
        "full_name": user["full_name"],
        "height": user["height"],
        "weight": user["weight"],
        "total_calories": user["total_calories"],
    }
