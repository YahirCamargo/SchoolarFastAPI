from sqlalchemy.orm import Session
from models.models_envios import Envio
from schemas.schema_envio import EnvioBase,EnvioActualizar

def get_envio(db:Session):
    return db.query(Envio).all()

def post_envio(db:Session,envio:EnvioBase):
    envio_a_crear = db.query().filter(Envio.numero_seguimiento == envio.numero_seguimiento).first()
    if envio_a_crear:
        return None
    nuevo_envio = Envio(
        fecha_entrega = envio.fecha_entrega,
        estado = envio.estado,
        numero_seguimiento = envio.numero_seguimiento,
        domicilios_id = envio.domicilios_id,
        pedidos_id = envio.pedidos_id
    )
    db.add(nuevo_envio)
    db.commit()
    db.refresh(nuevo_envio)
    return nuevo_envio

def patch_envios(db:Session,envio_id:int,envio_actualizado:EnvioActualizar):
    envio_a_actualizar = db.query(Envio).filter(Envio.id == envio_id).first()
    if not envio_a_actualizar:
        return None
    
    update_data = envio_actualizado.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(envio_a_actualizar, key, value)
    db.commit()
    db.refresh(envio_a_actualizar)
    return envio_a_actualizar

def delete_envios(db:Session,envio_id:int):
    envio_a_borrar = db.query(Envio).filter(Envio.id == envio_id).first()
    if not envio_a_borrar:
        return None
    db.delete(envio_a_borrar)
    db.commit()
    return envio_a_borrar