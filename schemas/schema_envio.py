from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EnvioBase(BaseModel):
    fecha_entrega : Optional[datetime] = None
    estado: str #dejar pendiente
    numero_seguimiento : str=Field(...,max_length=20)
    domicilios_id : int
    pedidos_id : int

class EnvioActualizar(BaseModel):
    fecha_entrega : Optional[datetime]
    estado: Optional[str] #dejar pendiente
    numero_seguimiento : Optional[str]=Field(None,max_length=20)

class EnviosResponder(EnvioBase):
    id : int
    fecha : datetime
    
    class Config:
        from_attributes = True



"""
    id = Column(SMALLINT(unsigned=True),nullable=False,autoincrement=True,primary_key=True)
    fecha_entrega = Column(DATETIME(),nullable=True)
    fecha = Column(DATETIME, nullable=False, server_default=func.now())
    estado = Column(Enum(EstadoEnum),nullable=False,default='Pendiente')
    numero_seguimiento = Column(String(20), nullable=False, unique=True)
    domicilios_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("domicilios.id",ondelete="RESTRICT"),
        index=True,
        nullable=False
    )
    pedidos_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("pedidos.id",ondelete="CASCADE"),
        index=True,
        nullable=False
    )
"""