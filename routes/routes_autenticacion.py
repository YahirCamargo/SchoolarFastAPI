from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_usuarios import Usuario
from schemas.schema_usuario import UsuarioCrear, UsuarioResponder,UsuarioLogin
from core.seguridad import hashear_contraseña, verificar_contraseña, crear_token_acceso, CREDENTIALS_EXCEPTION
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from dependencies.dependencies_autenticacion import get_current_user


router = APIRouter(prefix="/auth",tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/register', response_model=UsuarioResponder,status_code=status.HTTP_201_CREATED)
def registrar(user: UsuarioCrear, db:Session=Depends(get_db)):
    existing_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    contraseña_hasheada = hashear_contraseña(user.contrasena)
    nuevo_usuario = Usuario(
        nombre=user.nombre, 
        email=user.email, 
        contrasena=contraseña_hasheada,
        telefono=user.telefono,
        sexo=user.sexo,
        fecha_nacimiento=user.fecha_nacimiento,
        rol='cliente'
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    
    if not user or not verificar_contraseña(form_data.password, user.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = crear_token_acceso({"sub": user.email,"user_id": user.id,"rol": user.rol})
    return {"access_token": token, "token_type": "bearer"}

@router.get('/perfil', response_model=UsuarioResponder)
def obtener_mi_perfil(current_user: Usuario = Depends(get_current_user)):
    return current_user