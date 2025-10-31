from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_usuarios import Usuario
from models.models_domicilios import Domicilios
from schemas.schema_domicilio import DomicilioBase,DomicilioActualizar,DomicilioResponder
from services.service_domicilio import get_domicilios,get_domicilios_por_id,post_domicilios,patch_domicilios,delete_domicilios
from starlette import status
from dependencies.dependencies_autenticacion import get_current_user

router = APIRouter(prefix="/addresses",tags=["Addresses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/',response_model=List[DomicilioResponder])
def obtener_domicilios(db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return get_domicilios(db,user_id=current_user.id)

@router.get('/{domicilio_id}',response_model=DomicilioResponder)
def obtener_domicilios_por_id(domicilio_id:str,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    domicilio = get_domicilios_por_id(db,domicilio_id,current_user.id)
    if not domicilio:
        raise HTTPException(status_code=404,detail="Domicilio no encontrado")
    return domicilio

@router.post('/',response_model=DomicilioResponder,status_code=status.HTTP_201_CREATED)
def crear_domicilios(domicilio:DomicilioBase,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    domicilio_a_crear = post_domicilios(db,domicilio,current_user.id)
    return domicilio_a_crear

# Checar bien esto y mejor usar patch
@router.put('/{domicilio_id}',response_model=DomicilioResponder)
def actualizar_domicilio(domicilio_id:str,domicilio:DomicilioActualizar,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    domicilio_a_actualizar = patch_domicilios(db,domicilio_id,domicilio,current_user.id)
    if not domicilio_a_actualizar:
        raise HTTPException(status_code=404,detail="Domicilio no encontrado")
    return domicilio_a_actualizar


@router.delete('/{domicilio_id}',response_model=DomicilioResponder)
def borrar_domicilio(domicilio_id:str,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    domicilio_a_borrar = delete_domicilios(db,domicilio_id,current_user.id)
    if not domicilio_a_borrar:
        raise HTTPException(status_code=404,detail="Domicilio no encontrado")
    return domicilio_a_borrar