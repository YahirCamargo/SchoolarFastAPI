from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.seguridad import verificar_token, CREDENTIALS_EXCEPTION
from models.models_usuarios import Usuario
from db.database import SessionLocal 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login") 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    
    payload = verificar_token(token, CREDENTIALS_EXCEPTION)
    email: str = payload.get("sub")

    user = db.query(Usuario).filter(Usuario.email == email).first()
    
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user