from sqlalchemy import Column, Numeric, ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT, TINYINT
from db.database import Base

class DetalleCarrito(Base):
    __tablename__ = "detalles_carrito"
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
        nullable=False,
        index=True
    )



"""
CREATE TABLE `detalles_carrito` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `cantidad` tinyint(3) unsigned NOT NULL DEFAULT '1',
  `precio` decimal(7,2) unsigned NOT NULL,
  `productos_id` smallint(5) unsigned NOT NULL,
  `usuarios_id` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_productos_idx` (`productos_id`),
  KEY `fk_usuarios_idx` (`usuarios_id`),
  CONSTRAINT `fk_productos_idx` FOREIGN KEY (`productos_id`) REFERENCES `productos` (`id`),
  CONSTRAINT `fk_usuarios_idx` FOREIGN KEY (`usuarios_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB
"""