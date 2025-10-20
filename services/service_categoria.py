from sqlalchemy.orm import Session
from models.models_categorias import Categoria
from schemas.schema_categoria import CategoriaBase

def get_categoria(db:Session):
    return db.query(Categoria).all()

def post_categoria(db:Session,categoria:CategoriaBase):
    resultado = db.query(Categoria).filter(Categoria.nombre == categoria.nombre).first()
    if resultado:
        return None
    
    nueva_categoria = Categoria(
        nombre = categoria.nombre
    )
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria

def put_categoria(db:Session,categoria_id:int,categoria_actualizada:CategoriaBase):
    categoria_a_actualizar = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria_a_actualizar:
        return None
    
    categoria_a_actualizar.nombre = categoria_actualizada.nombre
    db.commit()
    db.refresh(categoria_a_actualizar)
    return categoria_a_actualizar

def delete_categoria(db:Session,categoria_id):
    categoria_a_borrar = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria_a_borrar:
        return None
    db.delete(categoria_a_borrar)
    db.commit()
    return categoria_a_borrar