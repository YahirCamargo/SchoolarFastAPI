from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_detalles_carrito import DetalleCarrito
from schemas.schema_detalle_carrito import DetalleCarritoBase,DetalleCarritoActualizar,DetalleCarritoResponder
from services.service_detalle_carrito import get_detalle_carrito,post_detalle_carrito,patch_detalle_carrito,delete_detalle_carrito
from starlette import status

router = APIRouter(prefix="/detalles-carrito",tags=["Detalles Carrito"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/',response_model=List[DetalleCarritoResponder])
def obtener_detalles_carrito(db:Session=Depends(get_db)):
    return get_detalle_carrito(db)

@router.post('/',response_model=DetalleCarritoResponder,status_code=status.HTTP_201_CREATED)
def crear_detalles_carrito(detalle_carrito:DetalleCarritoBase,db:Session=Depends(get_db)):
    detalles_carrito_a_crear = post_detalle_carrito(db,detalle_carrito)
    return detalles_carrito_a_crear

@router.patch('/{detalle_pedido_id}',response_model=DetalleCarritoResponder)
def actualizar_detalles_carrito(detalle_pedido_id:int,detalle_carrito:DetalleCarritoActualizar,db:Session=Depends(get_db)):
    detalles_carrito_a_actualizar = post_detalle_carrito(db,detalle_carrito)
    if not detalles_carrito_a_actualizar:
        raise HTTPException(status_code=404,detail="Detalle de carrito no encontrado")
    return detalles_carrito_a_actualizar

@router.delete('/{detalle_pedido_id}',response_model=DetalleCarritoResponder)
def borrar_detalles_carrito(detalle_pedido_id:int,db:Session=Depends(get_db)):
    detalles_carrito_a_borrar = delete_detalle_carrito(db,detalle_pedido_id)
    if not detalles_carrito_a_borrar:
        raise HTTPException(status_code=404,detail="Detalle de carrito no encontrado")
    return detalles_carrito_a_borrar