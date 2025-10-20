from sqlalchemy.orm import Session
from models.models_detalles_pedido import DetallePedido
from schemas.schema_detalle_pedido import DetallePedidoBase,DetallePedidoActualizar

def get_detalles_pedido(db:Session):
    return db.query(DetallePedido).all()

def post_detalles_pedido(db:Session,detalle_pedido:DetallePedidoBase):
    detalle_pedido_a_crear = DetallePedido(
        cantidad=detalle_pedido.cantidad,
        precio=detalle_pedido.precio,
        productos_id = detalle_pedido.productos_id,
        pedidos_id = detalle_pedido.pedidos_id
    )
    db.add(detalle_pedido_a_crear)
    db.commit()
    db.refresh(detalle_pedido_a_crear)
    return detalle_pedido_a_crear

def patch_detalles_pedido(db:Session,detalle_pedido_id:int,detalle_pedido:DetallePedidoActualizar):
    detalle_pedido_a_actualizar = db.query(DetallePedido).filter(DetallePedido.id == detalle_pedido_id).first()
    if not detalle_pedido_a_actualizar:
        return None
    update_data = detalle_pedido.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(detalle_pedido_a_actualizar, key, value)
    db.commit()
    db.refresh(detalle_pedido_a_actualizar)
    return detalle_pedido_a_actualizar

def delete_detalles_pedido(db:Session,detalle_pedido_id:int):
    detalle_pedido_a_borrar = db.query(DetallePedido).filter(DetallePedido.id == detalle_pedido_id).first()
    if not detalle_pedido_a_borrar:
        return None
    db.delete(detalle_pedido_a_borrar)
    db.commit()
    return detalle_pedido_a_borrar