from sqlalchemy import Column, String, CHAR, Enum, Date, DateTime, func
from sqlalchemy.dialects.mysql import TINYINT
from db.database import Base
import enum

class SexoEnum(enum.Enum):
    H = "H"
    M = "M"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(TINYINT(unsigned=True), primary_key=True, nullable=False)
    nombre = Column(String(45), nullable=False)
    email = Column(String(60), unique=True, nullable=False)
    telefono = Column(CHAR(10))
    sexo = Column(Enum(SexoEnum), nullable=False) 
    fecha_nacimiento = Column(Date, nullable=False)
    contrasena = Column(CHAR(255), nullable=False)
    fecha_registro = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    rol = Column(String(20),default="cliente",nullable=False)

"""
CREATE TABLE `usuarios` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `email` varchar(60) NOT NULL,
  `telefono` char(10) NOT NULL,
  `sexo` enum('H','M') NOT NULL COMMENT 'H: Hombre, M: Mujer',
  `fecha_nacimiento` date NOT NULL,
  `contrasena` char(60) NOT NULL COMMENT 'Hash BCrypt',
  `fecha_registro` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `idx_email_unico` (`email`),
  KEY `idx_fecha_registro` (`fecha_registro`)
) ENGINE=InnoDB
"""
