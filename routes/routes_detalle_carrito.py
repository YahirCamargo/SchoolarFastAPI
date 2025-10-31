from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.models_usuarios import Usuario
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_detalles_carrito import DetalleCarrito
from schemas.schema_detalle_carrito import DetalleCarritoBase,DetalleCarritoActualizar,DetalleCarritoResponder
from services.service_detalle_carrito import get_detalle_carrito,get_detalle_carrito_por_id,post_detalle_carrito,patch_detalle_carrito,delete_detalle_carrito
from starlette import status
from dependencies.dependencies_autenticacion import get_current_user

router = APIRouter(prefix="/cart",tags=["Carts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/',response_model=List[DetalleCarritoResponder])
def obtener_detalles_carrito(db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return get_detalle_carrito(db,current_user.id)

@router.get('/{detalle_carrito_id}',response_model=DetalleCarritoResponder)
def obtener_detalles_carrito_por_id(detalle_carrito_id:str,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    detalle_carrito = get_detalle_carrito_por_id(db,detalle_carrito_id,current_user.id)
    if not detalle_carrito:
        raise HTTPException(status_code=404,detail="Detalle carrito no encontrado")
    return detalle_carrito

@router.post('/',response_model=DetalleCarritoResponder,status_code=status.HTTP_201_CREATED)
def crear_detalles_carrito(detalle_carrito:DetalleCarritoBase,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    detalles_carrito_a_crear = post_detalle_carrito(db,detalle_carrito,current_user.id)
    return detalles_carrito_a_crear

@router.patch('/{detalle_pedido_id}',response_model=DetalleCarritoResponder)
def actualizar_detalles_carrito(detalle_pedido_id:str,detalle_carrito:DetalleCarritoActualizar,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    detalles_carrito_a_actualizar = post_detalle_carrito(db,detalle_carrito,current_user.id)
    if not detalles_carrito_a_actualizar:
        raise HTTPException(status_code=404,detail="Detalle de carrito no encontrado")
    return detalles_carrito_a_actualizar

@router.delete('/{detalle_pedido_id}',response_model=DetalleCarritoResponder)
def borrar_detalles_carrito(detalle_pedido_id:str,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    detalles_carrito_a_borrar = delete_detalle_carrito(db,detalle_pedido_id,current_user.id)
    if not detalles_carrito_a_borrar:
        raise HTTPException(status_code=404,detail="Detalle de carrito no encontrado")
    return detalles_carrito_a_borrar