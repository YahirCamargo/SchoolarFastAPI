from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_usuarios import Usuario
from models.models_detalles_pedido import DetallePedido
from schemas.schema_detalle_pedido import DetallePedidoBase,DetallePedidoActualizar,DetallePedidoResponder
from services.service_detalle_pedido import get_detalles_pedido,get_detalles_pedido_por_id,post_detalles_pedido,patch_detalles_pedido,delete_detalles_pedido
from dependencies.dependencies_autenticacion import get_current_user
from starlette import status

router = APIRouter(prefix="/order-details",tags=["Order Details"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/',response_model=List[DetallePedidoResponder])
def obtener_detalle_pedido(db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return get_detalles_pedido(db,current_user.id)

@router.get('/{detalle_pedido_id}',response_model=DetallePedidoResponder)
def obtener_detalle_pedido_por_id(detalle_pedido_id:str,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    detalle_pedido = get_detalles_pedido_por_id(db,detalle_pedido_id,current_user.id)
    if not detalle_pedido:
        raise HTTPException(status_code=404,detail="Detalle pedido no encontrado")
    return detalle_pedido


@router.post('/',response_model=DetallePedidoResponder,status_code=status.HTTP_201_CREATED)
def crear_detalle_pedido(detalle_pedido:DetallePedidoBase,db:Session=Depends(get_db)):
    detalle_pedido_a_crear = post_detalles_pedido(db,detalle_pedido)
    return detalle_pedido_a_crear

@router.patch('/{detalle_pedido_id}',response_model=DetallePedidoResponder)
def actualizar_detalle_pedido(detalle_pedido_id:str,detalle_pedido:DetallePedidoActualizar,db:Session=Depends(get_db)):
    detalle_pedido_a_actualizar = patch_detalles_pedido(db,detalle_pedido_id,detalle_pedido)
    if not detalle_pedido_a_actualizar:
        raise HTTPException(status_code=404,detail="Detalle de pedido no encontrado")
    return detalle_pedido_a_actualizar

@router.delete('/{detalle_pedido_id}',response_model=DetallePedidoResponder)
def actualizar_detalle_pedido(detalle_pedido_id:str,db:Session=Depends(get_db)):
    detalle_pedido_a_borrar = delete_detalles_pedido(db,detalle_pedido_id)
    if not detalle_pedido_a_borrar:
        raise HTTPException(status_code=404,detail="Detalle de pedido no encontrado")
    return detalle_pedido_a_borrar