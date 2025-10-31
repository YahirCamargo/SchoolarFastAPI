from sqlalchemy.orm import Session
from models.models_envios import Envio
from models.models_domicilios import Domicilios
from models.models_pedidos import Pedido
from schemas.schema_envio import EnvioBase,EnvioActualizar
from typing import List

def get_envio(db:Session,user_id:str) -> List[Envio]:
    envios =  db.query(Envio).join(
        Pedido, 
        Envio.pedidos_id == Pedido.id 
    ).filter(
        Pedido.usuarios_id == user_id
    ).all()
    return envios

def get_envio_por_id(db:Session,envio_id:int,user_id:str):
    envio = db.query(Envio).join(
        Pedido,
        Envio.pedidos_id == Pedido.id
    ).filter(
        Pedido.usuarios_id == user_id,
        Envio.id == envio_id
    ).first()

    if not envio:
        raise None
    return envio


# Poner logica para que si no existe ningun domicilio le diga que no puede hacer el envio
def post_envio(db:Session,envio:EnvioBase,user_id:str):
    envio_a_crear = db.query().filter(Envio.numero_seguimiento == envio.numero_seguimiento).first()
    domicilio_preferido_id = db.query(Domicilios).filter(Domicilios.usuarios_id == user_id, Domicilios.preferido == True).first()
    if envio_a_crear:
        return None
    nuevo_envio = Envio(
        fecha_entrega = envio.fecha_entrega,
        estado = envio.estado,
        numero_seguimiento = envio.numero_seguimiento,
        domicilios_id = domicilio_preferido_id,
        pedidos_id = envio.pedidos_id
    )
    db.add(nuevo_envio)
    db.commit()
    db.refresh(nuevo_envio)
    return nuevo_envio

def patch_envios(db:Session,envio_id:int,envio_actualizado:EnvioActualizar,user_id:str):
    envio_a_actualizar = db.query(Envio).filter(Envio.id == envio_id).first()
    if not envio_a_actualizar:
        return None
    
    update_data = envio_actualizado.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(envio_a_actualizar, key, value)
    db.commit()
    db.refresh(envio_a_actualizar)
    return envio_a_actualizar

def delete_envios(db:Session,envio_id:int,user_id:str):
    envio_a_borrar = db.query(Envio).filter(Envio.id == envio_id).first()
    if not envio_a_borrar:
        return None
    db.delete(envio_a_borrar)
    db.commit()
    return envio_a_borrar