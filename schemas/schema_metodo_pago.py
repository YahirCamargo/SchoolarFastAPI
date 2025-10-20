from pydantic import BaseModel, Field
from decimal import Decimal

class MetodoPagoBase(BaseModel):
    nombre:str
    comision:Decimal=Field(...,decimal_places=2,le=Decimal("99.99"))


class MetodoPagoResponder(MetodoPagoBase):
    id:int

    class Config:
        from_attributes = True