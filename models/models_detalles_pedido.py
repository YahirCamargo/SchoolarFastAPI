from sqlalchemy import Column, Numeric, ForeignKey, Index, CheckConstraint
from sqlalchemy.dialects.mysql import SMALLINT, TINYINT
from db.database import Base


class DetallePedido(Base):
    __tablename__ = "detalles_pedido"
    id = Column(SMALLINT(unsigned=True),nullable=False,autoincrement=True,primary_key=True)
    cantidad = Column(TINYINT(unsigned=True),nullable=False)
    precio = Column(Numeric(7,2),nullable=False)
    productos_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("productos.id",onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    pedidos_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("pedidos.id",ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    __table_args__ = (
        Index('idx_pedido_producto', 'pedidos_id', 'productos_id'),
        CheckConstraint('cantidad > 0', name='detalles_pedido_chk_1'),
    )




"""
CREATE TABLE `detalles_pedido` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `cantidad` tinyint(3) unsigned NOT NULL,
  `precio` decimal(7,2) NOT NULL,
  `productos_id` smallint(5) unsigned NOT NULL,
  `pedidos_id` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_productos_idx` (`productos_id`),
  KEY `idx_pedido_producto` (`pedidos_id`,`productos_id`),
  CONSTRAINT `fk_detalles_pedido_pedidos` FOREIGN KEY (`pedidos_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_detalles_pedido_productos` FOREIGN KEY (`productos_id`) REFERENCES `productos` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `detalles_pedido_chk_1` CHECK ((`cantidad` > 0))
) ENGINE=InnoDB
"""