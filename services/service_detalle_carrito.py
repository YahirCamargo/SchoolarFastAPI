from sqlalchemy.orm import Session
from typing import List
from models.models_detalles_carrito import DetalleCarrito
from schemas.schema_detalle_carrito import DetalleCarritoBase,DetalleCarritoActualizar

def get_detalle_carrito(db:Session,user_id:str) -> List[DetalleCarrito]:
    return db.query(DetalleCarrito).filter(DetalleCarrito.usuarios_id == user_id).all()

def get_detalle_carrito_por_id(db:Session,detalle_carrito_id,user_id:str):
    detalle_carrito = db.query(DetalleCarrito).filter(DetalleCarrito.usuarios_id == user_id,DetalleCarrito.id == detalle_carrito_id).first()
    if not detalle_carrito:
        return None
    return detalle_carrito

def post_detalle_carrito(db:Session,detalle_carrito:DetalleCarritoBase,user_id:str):
    detalle_carrito_a_crear = DetalleCarrito(
        cantidad = detalle_carrito.cantidad,
        precio = detalle_carrito.precio,
        productos_id = detalle_carrito.productos_id,
        usuarios_id = user_id
    )
    db.add(detalle_carrito_a_crear)
    db.commit()
    db.refresh(detalle_carrito_a_crear)
    return detalle_carrito_a_crear

def patch_detalle_carrito(db:Session,detalle_carrito_id:int,detalle_carrito_actualizado:DetalleCarritoActualizar,user_id:str):
    detalle_carrito_a_actualizar = db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_carrito_id,DetalleCarrito.usuarios_id == user_id).first()

    if not detalle_carrito_a_actualizar:
        return None
    
    update_data = detalle_carrito_actualizado.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(detalle_carrito_a_actualizar, key, value)

    db.commit()
    db.refresh(detalle_carrito_a_actualizar)
    return detalle_carrito_a_actualizar

def delete_detalle_carrito(db:Session,detalle_carrito_id:int,user_id:str):
    detalle_carrito_a_borrar = db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_carrito_id,DetalleCarrito.usuarios_id == user_id).first()

    if not detalle_carrito_a_borrar:
        return None
    db.delete(detalle_carrito_a_borrar)
    db.commit()
    return detalle_carrito_a_borrar