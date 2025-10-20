from sqlalchemy.orm import Session
from models.models_metodos_pago import MetodoPago
from schemas.schema_metodo_pago import MetodoPagoBase

def obtener_metodo_pago(db:Session):
    return db.query(MetodoPago).all()

def crear_metodo_pago(db:Session,metodo:MetodoPagoBase):
    metodo_a_crear = db.query(MetodoPago).filter(MetodoPago.nombre == metodo.nombre).first()
    if metodo_a_crear:
        return None
    
    nuevo_metodo_pago = MetodoPago(
        nombre=metodo.nombre,
        comision=metodo.comision
    )
    db.add(nuevo_metodo_pago)
    db.commit()
    db.refresh(nuevo_metodo_pago)
    return nuevo_metodo_pago

def actualizar_metodo_pago(metodo_id:int,metodo_actualizado:MetodoPagoBase,db:Session):
    metodo_a_actualizar = db.query(MetodoPago).filter(MetodoPago.id == metodo_id).first()
    if not metodo_a_actualizar:
        return None
    metodo_a_actualizar.nombre=metodo_actualizado.nombre
    metodo_a_actualizar.comision=metodo_actualizado.comision
    db.commit()
    db.refresh(metodo_a_actualizar)
    return metodo_a_actualizar

def borrar_metodo_pago(db:Session,metodo_id:int):
    metodo_a_borrar = db.query(MetodoPago).filter(MetodoPago.id == metodo_id).first()
    if not metodo_a_borrar:
        return None
    db.delete(metodo_a_borrar)
    db.commit()
    return metodo_a_borrar
