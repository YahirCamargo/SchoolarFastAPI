from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_domicilios import Domicilios
from schemas.schema_domicilio import DomicilioBase,DomicilioActualizar,DomicilioResponder
from services.service_domicilio import get_domicilios,post_domicilios,patch_domicilios,delete_domicilios
from starlette import status

router = APIRouter(prefix="/domicilios",tags=["Domicilios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/',response_model=List[DomicilioResponder])
def obtener_domicilios(db:Session=Depends(get_db)):
    return get_domicilios(db)

@router.post('/',response_model=DomicilioResponder,status_code=status.HTTP_201_CREATED)
def crear_domicilios(domicilio:DomicilioBase,db:Session=Depends(get_db)):
    domicilio_a_crear = post_domicilios(db,domicilio)
    return domicilio_a_crear

# Checar bien esto y mejor usar patch
@router.put('/{domicilio_id}',response_model=DomicilioResponder)
def actualizar_domicilio(domicilio_id:int,domicilio:DomicilioActualizar,db:Session=Depends(get_db)):
    domicilio_a_actualizar = patch_domicilios(db,domicilio_id,domicilio)
    if not domicilio_a_actualizar:
        raise HTTPException(status_code=404,detail="Domicilio no encontrado")
    return domicilio_a_actualizar


@router.delete('/{domicilio_id}',response_model=DomicilioResponder)
def actualizar_domicilio(domicilio_id:int,db:Session=Depends(get_db)):
    domicilio_a_borrar = delete_domicilios(db,domicilio_id)
    if not domicilio_a_borrar:
        raise HTTPException(status_code=404,detail="Domicilio no encontrado")
    return domicilio_a_borrar