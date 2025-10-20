from sqlalchemy import Column, DATETIME, String, Index, func, Enum, ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT
from db.database import Base
import enum

class EstadoEnum(enum.Enum):
    PENDIENTE = "PENDIENTE"
    EN_TRANSITO = "EN_TRANSITO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"

class Envio(Base):
    __tablename__ = "envios"
    id = Column(SMALLINT(unsigned=True),nullable=False,autoincrement=True,primary_key=True)
    fecha_entrega = Column(DATETIME(),nullable=True)
    fecha = Column(DATETIME, nullable=False, server_default=func.now())
    estado = Column(Enum(EstadoEnum),nullable=False,default='PENDIENTE')
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
CREATE TABLE `envios` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `fecha_entrega` datetime DEFAULT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('PENDIENTE','EN_TRANSITO','ENTREGADO','CANCELADO') NOT NULL DEFAULT 'PENDIENTE',
  `numero_seguimiento` varchar(20) NOT NULL,
  `domicilios_id` smallint(5) unsigned NOT NULL,
  `pedidos_id` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_seguimiento_UNIQUE` (`numero_seguimiento`),
  KEY `idx_estado` (`estado`),
  KEY `idx_fecha_entrega` (`fecha_entrega`),
  KEY `fk_envios_domicilios` (`domicilios_id`),
  KEY `fk_envios_pedidos` (`pedidos_id`),
  CONSTRAINT `fk_envios_domicilios` FOREIGN KEY (`domicilios_id`) REFERENCES `domicilios` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `fk_envios_pedidos` FOREIGN KEY (`pedidos_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB
"""