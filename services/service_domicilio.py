from sqlalchemy.orm import Session
from models.models_domicilios import Domicilios
from schemas.schema_domicilio import DomicilioBase,DomicilioActualizar
from typing import List

def get_domicilios(db:Session,user_id:str)-> List[Domicilios]:
    return db.query(Domicilios).filter(Domicilios.usuarios_id == user_id).all()

def get_domicilios_por_id(db:Session,domicilio_id:int,user_id:str):
    domicilio = db.query(Domicilios).filter(Domicilios.usuarios_id == user_id, Domicilios.id == domicilio_id).first()
    if not domicilio:
        return None
    return domicilio

# Checar bien para saber si evitar domicilios repetidos
# Cambiar la logica para que pueda enviar el usuarios_id de forma directa, de forma optional
def post_domicilios(db:Session,domicilio:DomicilioBase,user_id:str):
    numero_de_domicilios = db.query(Domicilios).filter(Domicilios.usuarios_id == user_id).count()

    es_preferido = (numero_de_domicilios == 0)

    domicilio_a_crear = Domicilios(
        calle = domicilio.calle,
        numero = domicilio.numero,
        colonia = domicilio.colonia,
        cp = domicilio.cp,
        estado = domicilio.estado,
        ciudad = domicilio.ciudad,
        usuarios_id = user_id,
        preferido = es_preferido
    )
    db.add(domicilio_a_crear)
    db.commit()
    db.refresh(domicilio_a_crear)
    return domicilio_a_crear

def patch_domicilios(db: Session, domicilio_id: int, domicilio_actualizado: DomicilioActualizar, user_id):
    domicilio_query = db.query(Domicilios).filter(
        Domicilios.id == domicilio_id,
        Domicilios.usuarios_id == user_id
    )
    domicilio_obj = domicilio_query.first()
    
    if not domicilio_obj:
        return None
    
    update_data = domicilio_actualizado.model_dump(exclude_unset=True)

    if 'preferido' in update_data and update_data['preferido'] == True:
        db.query(Domicilios).filter(
            Domicilios.usuarios_id == user_id,
            Domicilios.id != domicilio_id
        ).update(
            {"preferido": False}, 
            synchronize_session=False
        )

    for key, value in update_data.items():
        setattr(domicilio_obj, key, value)

    db.commit()
    db.refresh(domicilio_obj)
    return domicilio_obj

def delete_domicilios(db:Session,domicilio_id:int,user_id:str):
    domicilio_a_borrar = db.query(Domicilios).filter(Domicilios.id == domicilio_id,Domicilios.usuarios_id == user_id).first()
    if not domicilio_a_borrar:
        return None
    db.delete(domicilio_a_borrar)
    db.commit()
    return domicilio_a_borrar