# Módulo de autenticación para LogiXport
import bcrypt
from datetime import datetime, timedelta
import jwt
from sqlalchemy.orm import Session
from .models_sqlalchemy import Usuario, get_session
import logging
import socket

# Configurar logging
logger = logging.getLogger("auth")

# Configuración para JWT
SECRET_KEY = "logixport_secret_key_2023"  # En producción, usar una clave segura y almacenada en variables de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro para la contraseña proporcionada.
    """
    # Generar un salt y hashear la contraseña
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña proporcionada coincide con el hash almacenado.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(email: str, password: str) -> Usuario:
    """
    Autentica a un usuario verificando sus credenciales.
    Retorna el objeto Usuario si la autenticación es exitosa, None en caso contrario.
    """
    session = get_session()
    try:
        # Buscar usuario por correo electrónico
        usuario = session.query(Usuario).filter(Usuario.correo == email).first()
        
        # Verificar si el usuario existe y la contraseña es correcta
        if usuario and verify_password(password, usuario.contrasena_hash):
            return usuario
        return None
    except Exception as e:
        logger.error(f"Error en autenticación: {e}")
        return None
    finally:
        session.close()

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Crea un token JWT con los datos proporcionados y una fecha de expiración.
    """
    to_encode = data.copy()
    
    # Establecer tiempo de expiración
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Codificar el token JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def update_last_login(usuario_id: int, ip_address: str = None) -> bool:
    """
    Actualiza la información de último ingreso del usuario.
    """
    session = get_session()
    try:
        # Obtener usuario
        usuario = session.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        if not usuario:
            return False
        
        # Actualizar campos
        usuario.ultimo_ingreso = datetime.now()
        if ip_address:
            usuario.ip_ultima_sesion = ip_address
        
        # Guardar cambios
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Error al actualizar último ingreso: {e}")
        return False
    finally:
        session.close()

def get_user_by_id(usuario_id: int) -> Usuario:
    """
    Obtiene un usuario por su ID.
    """
    session = get_session()
    try:
        return session.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    except Exception as e:
        logger.error(f"Error al obtener usuario por ID: {e}")
        return None
    finally:
        session.close()

def get_user_by_email(email: str) -> Usuario:
    """
    Obtiene un usuario por su correo electrónico.
    """
    session = get_session()
    try:
        return session.query(Usuario).filter(Usuario.correo == email).first()
    except Exception as e:
        logger.error(f"Error al obtener usuario por email: {e}")
        return None
    finally:
        session.close()

def get_current_user(token: str) -> Usuario:
    """
    Obtiene el usuario actual a partir de un token JWT.
    Retorna el objeto Usuario si el token es válido, None en caso contrario.
    """
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id: int = payload.get("sub")
        
        if usuario_id is None:
            return None
        
        # Obtener usuario de la base de datos
        usuario = get_user_by_id(usuario_id)
        if usuario is None or not usuario.activo:
            return None
        
        return usuario
    except jwt.PyJWTError as e:
        logger.error(f"Error al decodificar token: {e}")
        return None
    except Exception as e:
        logger.error(f"Error al obtener usuario desde token: {e}")
        return None