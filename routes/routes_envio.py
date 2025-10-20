from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_envios import Envio
from schemas.schema_envio import EnvioBase,EnvioActualizar,EnviosResponder
from services.service_envio import get_envio,post_envio,patch_envios,delete_envios
from starlette import status

router = APIRouter(prefix="/envios",tags=["Envios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/',response_model=List[EnviosResponder])
def obtener_envios(db:Session=Depends(get_db)):
    return get_envio(db)

@router.post('/',response_model=EnviosResponder,status_code=status.HTTP_201_CREATED)
def crear_envios(envio:EnvioBase,db:Session=Depends(get_db)):
    envios_a_crear = post_envio(db,envio)
    if not envios_a_crear:
        raise HTTPException(status_code=400,detail="Numero de seguimiento existente")

# Checar bien esto y mejor usar patch
@router.patch('/{envio_id}',response_model=EnviosResponder)
def actualizar_envios(envio_id:int,envio_actualizado:EnvioActualizar,db:Session=Depends(get_db)):
    envio_a_actualizar = patch_envios(db,envio_id,envio_actualizado)
    if not envio_a_actualizar:
        raise HTTPException(status_code=404,detail="Envio no encontrado")
    return envio_a_actualizar


@router.delete('/{envio_id}',response_model=EnviosResponder)
def borrar_envios(envio_id:int,db:Session=Depends(get_db)):
    envio_a_borrar = delete_envios(db,envio_id)
    if not envio_a_borrar:
        raise HTTPException(status_code=404,detail="Envio no encontrado")
    return envio_a_borrar