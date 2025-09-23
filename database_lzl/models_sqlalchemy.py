from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Date, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from pathlib import Path

# Crear la base para los modelos declarativos
Base = declarative_base()

# Definición de la clase Usuario
class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    correo = Column(String(320), unique=True, nullable=False, index=True)
    nombre_usuario = Column(String(50), unique=True, nullable=True)
    contrasena_hash = Column(String(256), nullable=False)
    activo = Column(Boolean, default=True)
    rol = Column(String(50), default="usuario")
    empresa = Column(String(100), nullable=True)  # Nombre de empresa
    ip_ultima_sesion = Column(String(45), nullable=True)  # IPv4/IPv6
    membresia_activa = Column(Boolean, default=False)  # ¿Tiene membresía activa?
    plan_membresia = Column(String(50), nullable=True)  # Tipo de plan
    fecha_expiracion_membresia = Column(DateTime(timezone=True), nullable=True)  # Expiración de membresía
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    ultimo_ingreso = Column(DateTime(timezone=True), nullable=True)
    telefono = Column(String(20), nullable=True)
    avatar = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, correo='{self.correo}', nombre_usuario='{self.nombre_usuario}')>"

# Definición de las clases para el banco de datos legales y normativos

# Tabla para categorías de normatividad
class CategoriaNormativa(Base):
    __tablename__ = "categorias_normativas"
    
    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con documentos normativos
    documentos = relationship("DocumentoNormativo", back_populates="categoria")
    
    def __repr__(self):
        return f"<CategoriaNormativa(id={self.id_categoria}, nombre='{self.nombre}')>"

# Tabla para documentos normativos (leyes, tratados, reglamentos, etc.)
class DocumentoNormativo(Base):
    __tablename__ = "documentos_normativos"
    
    id_documento = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    id_categoria = Column(Integer, ForeignKey("categorias_normativas.id_categoria"), nullable=False)
    tipo_documento = Column(String(50), nullable=False)  # TLC, Ley, Reglamento, Decreto, Acuerdo, etc.
    fecha_publicacion = Column(Date, nullable=True)
    fecha_vigencia = Column(Date, nullable=True)
    contenido = Column(Text, nullable=True)
    url_documento = Column(String(255), nullable=True)  # URL al documento original si existe
    clave_referencia = Column(String(100), nullable=True, index=True)  # Clave única para referencia
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    categoria = relationship("CategoriaNormativa", back_populates="documentos")
    referencias = relationship("ReferenciaDocumento", back_populates="documento_origen", foreign_keys="ReferenciaDocumento.id_documento_origen")
    
    def __repr__(self):
        return f"<DocumentoNormativo(id={self.id_documento}, titulo='{self.titulo}', tipo='{self.tipo_documento}')>"

# Tabla para referencias entre documentos (correlaciones)
class ReferenciaDocumento(Base):
    __tablename__ = "referencias_documentos"
    
    id_referencia = Column(Integer, primary_key=True, autoincrement=True)
    id_documento_origen = Column(Integer, ForeignKey("documentos_normativos.id_documento"), nullable=False)
    id_documento_referenciado = Column(Integer, ForeignKey("documentos_normativos.id_documento"), nullable=False)
    tipo_referencia = Column(String(50), nullable=True)  # Modifica, Deroga, Complementa, etc.
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    documento_origen = relationship("DocumentoNormativo", foreign_keys=[id_documento_origen], back_populates="referencias")
    documento_referenciado = relationship("DocumentoNormativo", foreign_keys=[id_documento_referenciado])
    
    def __repr__(self):
        return f"<ReferenciaDocumento(id={self.id_referencia}, origen={self.id_documento_origen}, referencia={self.id_documento_referenciado})>"

# Tabla para la Tarifa de la LIGIE (actual e histórica)
class TarifaLIGIE(Base):
    __tablename__ = "tarifas_ligie"
    
    id_tarifa = Column(Integer, primary_key=True, autoincrement=True)
    fraccion_arancelaria = Column(String(20), nullable=False, index=True)
    descripcion = Column(Text, nullable=False)
    unidad_medida = Column(String(50), nullable=True)
    arancel_general = Column(String(20), nullable=True)
    version_tarifa = Column(String(20), nullable=False)  # 2022, 2020, 2007, 2002, 1995
    fecha_vigencia = Column(Date, nullable=True)
    notas = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<TarifaLIGIE(id={self.id_tarifa}, fraccion='{self.fraccion_arancelaria}', version='{self.version_tarifa}')>"

# Tabla para INCOTERMS
class Incoterm(Base):
    __tablename__ = "incoterms"
    
    id_incoterm = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(10), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    responsabilidades_vendedor = Column(Text, nullable=True)
    responsabilidades_comprador = Column(Text, nullable=True)
    version = Column(String(20), nullable=True)  # 2020, 2010, etc.
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Incoterm(id={self.id_incoterm}, codigo='{self.codigo}')>"

# Tabla para Complementos (circulares, boletines, jurisprudencias, etc.)
class Complemento(Base):
    __tablename__ = "complementos"
    
    id_complemento = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    tipo_complemento = Column(String(50), nullable=False)  # Circular, Boletín, Jurisprudencia, Hoja Informativa
    numero_referencia = Column(String(100), nullable=True, index=True)  # Número de circular, boletín, etc.
    fecha_publicacion = Column(Date, nullable=True)
    contenido = Column(Text, nullable=True)
    url_documento = Column(String(255), nullable=True)
    entidad_emisora = Column(String(100), nullable=True)  # Entidad que emite el documento
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Complemento(id={self.id_complemento}, titulo='{self.titulo}', tipo='{self.tipo_complemento}')>"

# Configuración de la conexión a la base de datos
def get_engine():
    """
    Crea y devuelve un motor de SQLAlchemy para la conexión a la base de datos.
    Utiliza los mismos parámetros de conexión que el módulo db_connection.py
    """
    # Parámetros de conexión (mismos que en db_connection.py)
    host = "localhost"
    database = "Db_LogiXport"
    user = "postgres"
    password = "Dork0909"
    port = "5432"
    
    # URL de conexión para SQLAlchemy
    DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    
    # Crear y devolver el motor
    return create_engine(DATABASE_URL)

def get_session():
    """
    Crea y devuelve una sesión de SQLAlchemy.
    """
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def create_tables():
    """
    Crea todas las tablas definidas en los modelos si no existen.
    """
    engine = get_engine()
    Base.metadata.create_all(engine)

# Si este archivo se ejecuta directamente, crear las tablas
if __name__ == "__main__":
    create_tables()
    print("Tablas creadas correctamente.")