from pydantic import BaseModel, Field
from typing import Optional

class DomicilioBase(BaseModel):
    calle:str=Field(...,max_length=45)
    numero:str=Field(...,max_length=10)
    colonia:str=Field(...,max_length=30)
    cp:str=Field(...,min_length=5,max_length=5)
    estado:str=Field(...,max_length=20)
    ciudad:str=Field(...,max_length=45)
    usuarios_id:int

class DomicilioActualizar(BaseModel):
    calle: Optional[str] = Field(None, max_length=45) 
    numero: Optional[str] = Field(None, max_length=10)
    colonia: Optional[str] = Field(None, max_length=30)
    cp: Optional[str] = Field(None, max_length=5)
    estado: Optional[str] = Field(None, max_length=20)
    ciudad: Optional[str] = Field(None, max_length=45)
    usuarios_id: Optional[int] = None

class DomicilioResponder(DomicilioBase):
    id:int

    class Config():
        from_attributes=True


"""
id = Column(SMALLINT(unsigned=True), nullable=False, autoincrement=True, primary_key=True)
    calle = Column(String(45), nullable=False)
    numero = Column(String(10), nullable=False) #Ej: 123A, S/N, 456-B
    colonia = Column(String(30), nullable=False)
    cp = Column(CHAR(5), nullable=False)
    estado = Column(String(20), nullable=False)
    ciudad = Column(String(45),nullable=False)
    usuarios_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("usuarios.id",onupdate="CASCADE",ondelete="CASCADE"),
        index=True,
    )
"""