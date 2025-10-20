from pydantic import BaseModel, Field

class CategoriaBase(BaseModel):
    nombre:str=Field(max_length=40)

class CategoriaResponder(CategoriaBase):
    id:int

    class Config:
        from_attributes=True