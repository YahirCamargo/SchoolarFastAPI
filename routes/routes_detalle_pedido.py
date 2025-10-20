from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_detalles_pedido import DetallePedido
from schemas.schema_detalle_pedido import DetallePedidoBase,DetallePedidoActualizar,DetallePedidoResponder
from services.service_detalle_pedido import get_detalles_pedido,post_detalles_pedido,patch_detalles_pedido,delete_detalles_pedido
from starlette import status

router = APIRouter(prefix="/detalles-pedido",tags=["Detalles Pedido"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/',response_model=List[DetallePedidoResponder])
def obtener_detalle_pedido(db:Session=Depends(get_db)):
    return get_detalles_pedido(db)

@router.post('/',response_model=DetallePedidoResponder,status_code=status.HTTP_201_CREATED)
def crear_detalle_pedido(detalle_pedido:DetallePedidoBase,db:Session=Depends(get_db)):
    detalle_pedido_a_crear = post_detalles_pedido(db,detalle_pedido)
    return detalle_pedido_a_crear

@router.patch('/{detalle_pedido_id}',response_model=DetallePedidoResponder)
def actualizar_detalle_pedido(detalle_pedido_id:int,detalle_pedido:DetallePedidoActualizar,db:Session=Depends(get_db)):
    detalle_pedido_a_actualizar = patch_detalles_pedido(db,detalle_pedido_id,detalle_pedido)
    if not detalle_pedido_a_actualizar:
        raise HTTPException(status_code=404,detail="Detalle de pedido no encontrado")
    return detalle_pedido_a_actualizar

@router.delete('/{detalle_pedido_id}',response_model=DetallePedidoResponder)
def actualizar_detalle_pedido(detalle_pedido_id:int,db:Session=Depends(get_db)):
    detalle_pedido_a_borrar = delete_detalles_pedido(db,detalle_pedido_id)
    if not detalle_pedido_a_borrar:
        raise HTTPException(status_code=404,detail="Detalle de pedido no encontrado")
    return detalle_pedido_a_borrar