from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class DetalleCarritoBase(BaseModel):
    cantidad:int
    precio:Decimal=Field(...,decimal_places=2, le=Decimal("99999.99"))
    productos_id:int

class DetalleCarritoActualizar(BaseModel):
    cantidad:Optional[int]
    precio:Optional[Decimal]=Field(None,decimal_places=2,le=Decimal("99999.99"))
    productos_id: Optional[int] = None

class DetalleCarritoResponder(DetalleCarritoBase):
    id:str

    class Config:
        from_attributes=True
    



"""
 id = Column(SMALLINT(unsigned=True), primary_key=True, nullable=False, autoincrement=True)
    cantidad = Column(TINYINT(unsigned=True), nullable=False, default=1)
    precio = Column(Numeric(7,2), nullable=False)
    productos_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("productos.id"),
        nullable=False,
        index=True
    )
    usuarios_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("usuarios.id"),
        nulleable=False,
        index=True
    )
"""