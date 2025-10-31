from sqlalchemy import Column, String, ForeignKey, Index
from sqlalchemy.dialects.mysql import CHAR, SMALLINT, BOOLEAN
from db.database import Base

class Domicilios(Base):
    __tablename__ = "domicilios"
    id = Column(SMALLINT(unsigned=True), nullable=False, autoincrement=True, primary_key=True)
    calle = Column(String(45), nullable=False)
    numero = Column(String(10), nullable=False) #Ej: 123A, S/N, 456-B
    colonia = Column(String(30), nullable=False)
    cp = Column(CHAR(5), nullable=False)
    estado = Column(String(20), nullable=False)
    ciudad = Column(String(45),nullable=False)
    preferido = Column(BOOLEAN, nullable=False, default=False)
    usuarios_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("usuarios.id",onupdate="CASCADE",ondelete="CASCADE"),
        index=True,
    )
    __table_args__ = (
        Index('idx_estado_ciudad', 'estado', 'ciudad'),
    )


"""
CREATE TABLE `domicilios` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `calle` varchar(45) NOT NULL,
  `numero` varchar(10) NOT NULL COMMENT 'Ej: 123A, S/N, 456-B',
  `colonia` varchar(30) NOT NULL,
  `cp` char(5) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `ciudad` varchar(45) NOT NULL,
  `usuarios_id` smallint(5) unsigned NOT NULL,
  'preferido' BOOLEAN NOT NULL DEFAULT FALSE
  PRIMARY KEY (`id`),
  KEY `fk_domicilios_usuarios_idx` (`usuarios_id`),
  KEY `idx_estado_ciudad` (`estado`,`ciudad`),
  CONSTRAINT `fk_domicilios_usuarios` FOREIGN KEY (`usuarios_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB
"""