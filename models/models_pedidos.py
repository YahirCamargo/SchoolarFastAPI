from sqlalchemy import Column, DateTime, Numeric, func,ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT, CHAR, TINYINT
from db.database import Base

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(SMALLINT(unsigned=True), nullable=False, autoincrement=True, primary_key=True)
    fecha = Column(DateTime, nullable=False, server_default=func.now())
    numero = Column(CHAR(36),nullable=False,unique=True)
    importe_productos = Column(Numeric(10,2),nullable=False)
    importe_envio = Column(Numeric(6,2),nullable=False)
    fecha_hora_pago = Column(DateTime,nullable=True)
    usuarios_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("usuarios.id",ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    metodos_pago_id = Column(
        TINYINT(unsigned=True),
        ForeignKey("metodos_pago.id"),
        default='1',
        nullable=False,
        index=True,
    )

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
