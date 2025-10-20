from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_pedidos import Pedido
from schemas.schema_pedido import PedidoBase, PedidoActualizar, PedidoResponder
from services.service_pedido import get_pedido, post_pedido, patch_pedido, delete_pedido
from starlette import status

router = APIRouter(prefix="/pedido",tags=["Pedidos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/',response_model=List[PedidoResponder])
def obtener_pedidos(db:Session=Depends(get_db)):
    return get_pedido(db)

# Checar bien aqui para ver si le pongo alguna condicion al pedido
@router.post('/',response_model=PedidoResponder,status_code=status.HTTP_201_CREATED)
def crear_pedidos(pedido:PedidoBase,db:Session=Depends(get_db)):
    pedido_a_crear = post_pedido(db,pedido)
    return pedido_a_crear

@router.patch('/{pedido_id}',response_model=PedidoResponder)
def actualizar_pedidos(pedido_id:int,pedido:PedidoActualizar,db:Session=Depends(get_db)):
    pedido_a_actualizar = patch_pedido(db,pedido_id,pedido)
    if not pedido_a_actualizar:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido_a_actualizar

@router.delete('/{pedido_id}',response_model=PedidoResponder)
def eliminar_pedidos(pedido_id:int,db:Session=Depends(get_db)):
    pedido_a_eliminar = delete_pedido(db,pedido_id)
    if not pedido_a_eliminar:
        raise HTTPException(status_code=404,detail="Pedido no encontrado")