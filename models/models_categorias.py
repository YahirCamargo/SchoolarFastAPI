from sqlalchemy import Column, String, Index
from sqlalchemy.dialects.mysql import TINYINT 
from db.database import Base

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(TINYINT(unsigned=True),primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String(40), nullable=False)
    __table_args__ = (
        Index('idx_nombre_fulltext', nombre, mysql_using='fulltext'),
    )


"""
CREATE TABLE `categorias` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  FULLTEXT KEY `idx_nombre_fulltext` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""