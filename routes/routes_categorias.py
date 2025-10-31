from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_categorias import Categoria
from schemas.schema_categoria import CategoriaBase,CategoriaResponder
from services.service_categoria import get_categoria,post_categoria,put_categoria,delete_categoria
from starlette import status

router = APIRouter(prefix="/categories",tags=["Categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/',response_model=List[CategoriaResponder])
def obtener_categoria(db:Session=Depends(get_db)):
    return get_categoria(db)

@router.post('/',response_model=CategoriaResponder,status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria:CategoriaBase,db:Session=Depends(get_db)):
    categoria_a_crear = post_categoria(db,categoria)
    if not categoria_a_crear:
        raise HTTPException(status_code=400,detail="Categoria ya existente")
    return categoria_a_crear

@router.put('/{categoria_id}',response_model=CategoriaResponder)
def actualizar_categoria(categoria_id:str,categoria_actualizada:CategoriaBase,db:Session=Depends(get_db)):
    categoria_a_actualizar = put_categoria(db,categoria_id,categoria_actualizada)
    if not categoria_a_actualizar:
        raise HTTPException(status_code=404,detail="Categoria no encontrada")
    return categoria_a_actualizar

@router.delete('/{categoria_id}',response_model=CategoriaResponder)
def borrar_categoria(categoria_id:int,db:Session=Depends(get_db)):
    categoria_a_borrar = delete_categoria(db,categoria_id)
    if not categoria_a_borrar:
        raise HTTPException(status_code=404,detail="Categoria no encontrada")
    return categoria_a_borrar