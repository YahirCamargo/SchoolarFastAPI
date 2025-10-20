from sqlalchemy.orm import Session
from models.models_usuarios import Usuario
from schemas.schema_usuario import UsuarioCrear

def create_user(db: Session, user: UsuarioCrear):
    nuevo_usuario = Usuario(
        nombre=user.nombre, 
        email=user.email,
        contrasena=user.contrasena,
        telefono=user.telefono,
        sexo=user.sexo,
        fecha_nacimiento=user.fecha_nacimiento,
        )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def get_users(db: Session):
    return db.query(Usuario).all()

def get_users_by_id(item_id:int,db:Session):
    return db.query(Usuario).filter(Usuario.id == item_id).first()

def delete_user(db: Session, user_id: int):
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user

def update_user(db: Session, user_id: int, user_data: UsuarioCrear):
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        return None
    user.nombre = user_data.nombre
    user.email = user_data.email
    user.contrasena=user_data.contrasena
    user.telefono=user_data.telefono
    user.sexo=user_data.sexo
    user.fecha_nacimiento=user_data.fecha_nacimiento
    db.commit()
    db.refresh(user)
    return user
