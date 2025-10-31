from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_usuarios import Usuario
from schemas.schema_usuario import UsuarioCrear, UsuarioResponder
from services.service_usuario import create_user, get_users,get_users_by_id, delete_user, update_user

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/",response_model=List[UsuarioResponder])
def read(db: Session = Depends(get_db)):
    return get_users(db)

@router.get('/{user_id}',response_model=UsuarioResponder)
def read_by_id(user_id:str,db:Session = Depends(get_db)):
    user = get_users_by_id(user_id,db)
    if not user:
        raise(HTTPException(status_code=404,detail="Usuario no encontrado"))
    return user

@router.post("/",status_code=201)
def create(user: UsuarioCrear, db: Session = Depends(get_db)):
    return create_user(db,user)    

@router.put('/{user_id}',response_model=UsuarioResponder)
def update(user_id:str, user_data: UsuarioCrear, db: Session = Depends(get_db)):
    result = update_user(db,user_id,user_data)
    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return result

@router.delete('/{user_id}',status_code=204)
def erase(user_id:str,db:Session = Depends(get_db)):
    result = delete_user(db,user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return