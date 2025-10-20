from sqlalchemy import Column, String, Numeric
from sqlalchemy.dialects.mysql import TINYINT
from db.database import Base

class MetodoPago(Base):
    __tablename__ = "metodos_pago"
    id = Column(TINYINT(unsigned=True),primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String(25), nullable=False, index=True)
    comision = Column(Numeric(4,2),nullable=False, default=1.5)

"""
CREATE TABLE `metodos_pago` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `comision` decimal(4,2) NOT NULL DEFAULT '1.50',
  PRIMARY KEY (`id`),
  KEY `idx_nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""