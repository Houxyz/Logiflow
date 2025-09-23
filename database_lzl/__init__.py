# Database module for LogiXport
from .db_connection import connect_to_database, test_connection
from .db_models import BaseModel, User, Shipment

# Importar modelos SQLAlchemy
from .models_sqlalchemy import (
    Base, Usuario, get_engine, get_session, create_tables,
    CategoriaNormativa, DocumentoNormativo, ReferenciaDocumento, 
    TarifaLIGIE, Incoterm, Complemento
)

__all__ = [
    'connect_to_database', 'test_connection', 'BaseModel', 'User', 'Shipment',
    'Base', 'Usuario', 'get_engine', 'get_session', 'create_tables',
    'CategoriaNormativa', 'DocumentoNormativo', 'ReferenciaDocumento',
    'TarifaLIGIE', 'Incoterm', 'Complemento'
]