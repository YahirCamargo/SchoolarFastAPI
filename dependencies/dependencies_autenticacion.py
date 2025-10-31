from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.seguridad import verificar_token, CREDENTIALS_EXCEPTION
from models.models_usuarios import Usuario
from db.database import SessionLocal 
from starlette import status
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

    if email is None:
        raise CREDENTIALS_EXCEPTION

    user = db.query(Usuario).filter(Usuario.email == email).first()
    
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user

def admin_required(current_user: Usuario = Depends(get_current_user)):
    if current_user.rol != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos de administrador para acceder a este recurso."
        )
    return current_user