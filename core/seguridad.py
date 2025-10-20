from datetime import datetime,timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext
from pydantic_settings import BaseSettings
from fastapi import status, HTTPException

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No se pudieron validar las credenciales",
    headers={"WWW-Authenticate": "Bearer"},
)

class Settings(BaseSettings):
    mysql_user: str
    mysql_password: str
    mysql_host: str
    mysql_port: str
    mysql_db: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
contraseña_contexto = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hashear_contraseña(password: str) -> str:
    return contraseña_contexto.hash(password)

def verificar_contraseña(plain_password: str, hashed_password: str):
    return contraseña_contexto.verify(plain_password, hashed_password)

def crear_token_acceso(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expira = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expira})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def verificar_token(token:str,credenciales_excepcion:HTTPException = CREDENTIALS_EXCEPTION) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        username:str=payload.get("sub")
        if username is None:
            raise credenciales_excepcion
        
        return payload 
    except JWTError:
        raise credenciales_excepcion