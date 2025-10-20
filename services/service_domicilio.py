from sqlalchemy.orm import Session
from models.models_domicilios import Domicilios
from schemas.schema_domicilio import DomicilioBase,DomicilioActualizar

def get_domicilios(db:Session):
    return db.query(Domicilios).all()

# Checar bien para saber si evitar domicilios repetidos
def post_domicilios(db:Session,domicilio:DomicilioBase):
    domicilio_a_crear = Domicilios(
        calle = domicilio.calle,
        numero = domicilio.numero,
        colonia = domicilio.colonia,
        cp = domicilio.cp,
        estado = domicilio.estado,
        ciudad = domicilio.ciudad,
        usuarios_id = domicilio.usuarios_id
    )
    db.add(domicilio_a_crear)
    db.commit()
    db.refresh(domicilio_a_crear)
    return domicilio_a_crear

def patch_domicilios(db:Session,domicilio_id:int,domicilio_actualizado:DomicilioActualizar):
    domicilio_a_actualizar = db.query(Domicilios).filter(Domicilios.id == domicilio_id).first()
    if not domicilio_a_actualizar:
        return None
    update_data = domicilio_actualizado.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(domicilio_a_actualizar, key, value)

    db.commit()
    db.refresh(domicilio_a_actualizar)
    return domicilio_a_actualizar

def delete_domicilios(db:Session,domicilio_id:int):
    domicilio_a_borrar = db.query(Domicilios).filter(Domicilios.id == domicilio_id).first()
    if not domicilio_a_borrar:
        return None
    db.delete(domicilio_a_borrar)
    db.commit()
    return domicilio_a_borrar