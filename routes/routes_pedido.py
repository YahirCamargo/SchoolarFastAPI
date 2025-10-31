from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_usuarios import Usuario
from models.models_pedidos import Pedido
from schemas.schema_pedido import PedidoBase, PedidoActualizar, PedidoResponder, PedidoCheckout
from services.service_pedido import get_pedido,get_pedido_por_id, post_pedido, patch_pedido, delete_pedido
from starlette import status
from dependencies.dependencies_autenticacion import get_current_user

router = APIRouter(prefix="/orders",tags=["Orders"])
IMPORTE_ENVIO = 80.00

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/',response_model=List[PedidoResponder])
def obtener_pedidos(db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return get_pedido(db,current_user.id)

@router.get('/{pedido_id}',response_model=PedidoResponder)
def obtener_pedidos_por_id(pedido_id:str,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    pedido = get_pedido_por_id(db,pedido_id,current_user.id)
    if not pedido:
        raise HTTPException(status_code=404,detail="Pedido no encontrado")
    return pedido

# Checar bien aqui para ver si le pongo alguna condicion al pedido
@router.post('/',response_model=PedidoResponder,status_code=status.HTTP_201_CREATED)
def crear_pedidos(data: PedidoCheckout,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    nuevo_pedido = post_pedido(db,IMPORTE_ENVIO,data.metodos_pago_id,data.domicilios_id,current_user.id)

    if nuevo_pedido is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El carrito de compras está vacío. Agregue productos para crear un pedido.")
    # Aqui va el crear el registro de esto en envio
    
    
    return nuevo_pedido

@router.patch('/{pedido_id}',response_model=PedidoResponder)
def actualizar_pedidos(pedido_id:str,pedido:PedidoActualizar,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    pedido_a_actualizar = patch_pedido(db,pedido_id,pedido,current_user.id)
    if not pedido_a_actualizar:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido_a_actualizar

@router.delete('/{pedido_id}',response_model=PedidoResponder)
def eliminar_pedidos(pedido_id:str,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    pedido_a_eliminar = delete_pedido(db,pedido_id,current_user.id)
    if not pedido_a_eliminar:
        raise HTTPException(status_code=404,detail="Pedido no encontrado")