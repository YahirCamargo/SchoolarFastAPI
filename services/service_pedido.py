from sqlalchemy.orm import Session
from models.models_pedidos import Pedido
from schemas.schema_pedido import PedidoBase,PedidoActualizar


def get_pedido(db:Session):
    return db.query(Pedido).all()

def post_pedido(db:Session,pedido:PedidoBase):
    nuevo_pedido = Pedido(
        fecha=pedido.fecha,
        numero=pedido.numero,
        importe_productos=pedido.importe_productos,
        importe_envio=pedido.importe_envio,
        usuarios_id=pedido.usuarios_id,
        metodos_pago_id=pedido.metodos_pago_id,
        fecha_hora_pago=pedido.fecha_hora_pago
    )
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    return nuevo_pedido

def patch_pedido(db:Session,pedido_id:int,pedido:PedidoActualizar):
    pedido_a_actualizar = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido_a_actualizar:
        return None
    update_data = pedido.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(pedido_a_actualizar, key, value)

    db.commit()
    db.refresh(pedido_a_actualizar)
    return pedido_a_actualizar

def delete_pedido(db:Session,pedido_id:int):
    pedido_a_borrar = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido_a_borrar:
        return None
    db.delete(pedido_a_borrar)
    db.commit()
    return pedido_a_borrar