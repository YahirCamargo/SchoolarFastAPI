from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional

class PedidoBase(BaseModel):
    fecha:datetime
    numero:str=Field(max_length=36)
    importe_productos:Decimal=Field(...,decimal_places=2,le=Decimal("99999999.99"))
    importe_envio:Decimal=Field(...,decimal_places=2,le=Decimal("9999.99"))
    usuarios_id:int
    metodos_pago_id:int
    fecha_hora_pago:datetime | None

    class Config:
        json_encoders = {
            Decimal: lambda v: str(v),
            datetime: lambda v: v.isoformat()
        }

class PedidoActualizar(BaseModel):
    fecha:Optional[datetime]
    numero:Optional[str]=Field(max_length=36)
    importe_productos:Optional[Decimal]
    importe_envio:Optional[Decimal]
    fecha_hora_pago:Optional[datetime] | Optional[None]
    usuarios_id: Optional[int] = None
    metodos_pago_id: Optional[int] = None
    fecha_hora_pago: Optional[datetime] = None
    

    class Config:
        json_encoders = {
            Decimal: lambda v: str(v),
            datetime: lambda v: v.isoformat()
        }

class PedidoResponder(PedidoBase):
    id:int
    
    class Config:
        from_attributes=True

"""
CREATE TABLE `pedidos` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `numero` char(36) NOT NULL COMMENT 'UUID v4',
  `importe_productos` decimal(10,2) NOT NULL,
  `importe_envio` decimal(6,2) NOT NULL,
  `usuarios_id` smallint(5) unsigned NOT NULL,
  `metodos_pago_id` tinyint(3) unsigned NOT NULL DEFAULT '1',
  `fecha_hora_pago` datetime DEFAULT NULL,
  `importe_iva` decimal(7,2) GENERATED ALWAYS AS ((`importe_productos` * 0.16)) STORED,
  `total` decimal(8,2) GENERATED ALWAYS AS (((`importe_productos` + `importe_envio`) + `importe_iva`)) STORED,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_UNIQUE` (`numero`),
  KEY `idx_fecha` (`fecha`),
  KEY `idx_usuario_fecha` (`usuarios_id`,`fecha`),
  KEY `fk_pedidos_metodos_pago_idx` (`metodos_pago_id`),
  CONSTRAINT `fk_pedidos_metodos_pago` FOREIGN KEY (`metodos_pago_id`) REFERENCES `metodos_pago` (`id`),
  CONSTRAINT `fk_pedidos_usuarios` FOREIGN KEY (`usuarios_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB
"""