from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_envios import Envio
from models.models_usuarios import Usuario
from schemas.schema_envio import EnvioBase,EnvioActualizar,EnviosResponder
from services.service_envio import get_envio,get_envio_por_id,post_envio,patch_envios,delete_envios
from dependencies.dependencies_autenticacion  import get_current_user
from starlette import status

router = APIRouter(prefix="/shippings",tags=["Shippings"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/',response_model=List[EnviosResponder])
def obtener_envios(db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    envios =  get_envio(db,current_user.id)
    return envios

@router.get('/{envio_id}',response_model=EnviosResponder)
def obtener_envios(envio_id:str,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    envio = get_envio_por_id(db,envio_id,current_user.id)
    if not envio:
        raise HTTPException(status_code=404,detail="El envio no fue encontrado")
    return envio

@router.post('/',response_model=EnviosResponder,status_code=status.HTTP_201_CREATED)
def crear_envios(envio:EnvioBase,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    envios_a_crear = post_envio(db,envio,current_user.id)
    if not envios_a_crear:
        raise HTTPException(status_code=400,detail="Numero de seguimiento existente")

# Checar bien esto y mejor usar patch
@router.patch('/{envio_id}',response_model=EnviosResponder)
def actualizar_envios(envio_id:str,envio_actualizado:EnvioActualizar,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    envio_a_actualizar = patch_envios(db,envio_id,envio_actualizado,current_user.id)
    if not envio_a_actualizar:
        raise HTTPException(status_code=404,detail="Envio no encontrado")
    return envio_a_actualizar


@router.delete('/{envio_id}',response_model=EnviosResponder)
def borrar_envios(envio_id:str,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    envio_a_borrar = delete_envios(db,envio_id,current_user.id)
    if not envio_a_borrar:
        raise HTTPException(status_code=404,detail="Envio no encontrado")
    return envio_a_borrar