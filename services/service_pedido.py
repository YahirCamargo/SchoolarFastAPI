from sqlalchemy.orm import Session
from sqlalchemy import func,text
from models.models_pedidos import Pedido
from models.models_detalles_pedido import DetallePedido
from models.models_detalles_carrito import DetalleCarrito
from typing import List
import uuid


from schemas.schema_pedido import PedidoBase,PedidoActualizar

def get_pedido(db:Session,user_id:str)-> List[Pedido]:
    return db.query(Pedido).filter(Pedido.usuarios_id==user_id).all()

def get_pedido_por_id(db:Session,pedido_id:int,user_id:str):
    pedido_por_id = db.query(Pedido).filter(Pedido.usuarios_id == user_id, Pedido.id == pedido_id).first()
    if not pedido_por_id:
        return None
    return pedido_por_id


def post_pedido(db: Session, importe_envio: float, metodos_pago_id: int, domicilios_id: int, user_id: int):
    importe_productos = db.query(
        func.sum(DetalleCarrito.precio * DetalleCarrito.cantidad)
    ).filter(DetalleCarrito.usuarios_id == user_id).scalar()
    
    if not importe_productos:
        return None 
    
    try:
        nuevo_pedido = Pedido(
            numero=str(uuid.uuid4()),
            importe_productos=importe_productos,
            importe_envio=importe_envio,
            usuarios_id=user_id,
            domicilios_id=domicilios_id,
            metodos_pago_id=metodos_pago_id,
        )
        db.add(nuevo_pedido)
        db.flush()
        pedido_id = nuevo_pedido.id
        
        db.execute(text("""
            INSERT INTO detalles_pedido (pedidos_id, productos_id, cantidad, precio)
            SELECT 
                :p_id,                 
                productos_id,
                cantidad,
                precio
            FROM detalles_carrito
            WHERE usuarios_id = :u_id; 
        """), {"p_id": pedido_id, "u_id": user_id})
        
        db.query(DetalleCarrito).filter(DetalleCarrito.usuarios_id == user_id).delete()
        
        db.commit()
        db.refresh(nuevo_pedido)
        return nuevo_pedido
        
    except Exception as e:
        db.rollback() 
        raise e

def patch_pedido(db:Session,pedido_id:int,pedido:PedidoActualizar,user_id:str):
    pedido_a_actualizar = db.query(Pedido).filter(Pedido.id == pedido_id,Pedido.usuarios_id == user_id).first()
    if not pedido_a_actualizar:
        return None
    update_data = pedido.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(pedido_a_actualizar, key, value)

    db.commit()
    db.refresh(pedido_a_actualizar)
    return pedido_a_actualizar

def delete_pedido(db:Session,pedido_id:int,user_id:str):
    pedido_a_borrar = db.query(Pedido).filter(Pedido.id == pedido_id,Pedido.usuarios_id == user_id).first()
    
    if not pedido_a_borrar:
        return None
    db.delete(pedido_a_borrar)
    db.commit()
    return pedido_a_borrar