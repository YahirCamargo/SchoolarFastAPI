from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_metodos_pago import MetodoPago
from schemas.schema_metodo_pago import MetodoPagoBase,MetodoPagoResponder
from services.service_metodo_pago import obtener_metodo_pago,crear_metodo_pago,actualizar_metodo_pago,borrar_metodo_pago
from starlette import status

router = APIRouter(prefix="/metodos-pago",tags=["Metodos de Pago"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/',response_model=List[MetodoPagoResponder])
def leer_metodos_pago(db: Session = Depends(get_db)):
    return obtener_metodo_pago(db)

@router.post('/',response_model=MetodoPagoResponder,status_code=status.HTTP_201_CREATED)
def crear_metodos_pagp(metodo: MetodoPagoBase, db:Session=Depends(get_db)):
    resultado = crear_metodo_pago(db,metodo)
    if not resultado:
        raise HTTPException(status_code=400,detail="El metodo ya fue creado")
    return resultado

@router.put('/{metodo_id}',response_model=MetodoPagoResponder)
def actualizar_metodos_pago(metodo_id:int,metodo_actualizar:MetodoPagoBase,db:Session=Depends(get_db)):
    resultado = actualizar_metodo_pago(metodo_id,metodo_actualizar,db)
    if not resultado:
        raise HTTPException(status_code=404,detail="Metodo de pago no encontrado")
    return resultado

@router.delete('/{metodo_id}',response_model=MetodoPagoResponder)
def eliminar_metodo_pago(metodo_id:int,db:Session=Depends(get_db)):
    resultado = borrar_metodo_pago(db,metodo_id)
    if not resultado:
        raise HTTPException(status_code=404,detail="Metodo de pago no encontrado")
    return resultado
