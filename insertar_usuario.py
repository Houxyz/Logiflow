# Script para insertar un nuevo usuario en la base de datos
import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar módulos necesarios
from database_lzl.auth import get_password_hash
from database_lzl.models_sqlalchemy import Usuario, get_session
from datetime import datetime

def insertar_usuario(nombre_usuario, correo, contrasena, rol="usuario"):
    """
    Inserta un nuevo usuario en la base de datos.
    
    Args:
        nombre_usuario (str): Nombre de usuario
        correo (str): Correo electrónico
        contrasena (str): Contraseña en texto plano (será hasheada)
        rol (str): Rol del usuario (por defecto: "usuario")
    
    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario
    """
    # Crear una sesión de base de datos
    session = get_session()
    
    try:
        # Verificar si el usuario ya existe
        usuario_existente = session.query(Usuario).filter(
            (Usuario.correo == correo) | (Usuario.nombre_usuario == nombre_usuario)
        ).first()
        
        if usuario_existente:
            print(f"Error: Ya existe un usuario con el correo '{correo}' o nombre de usuario '{nombre_usuario}'")
            return False
        
        # Generar hash de la contraseña
        contrasena_hash = get_password_hash(contrasena)
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            nombre_usuario=nombre_usuario,
            correo=correo,
            contrasena_hash=contrasena_hash,
            rol=rol,
            activo=True,
            fecha_creacion=datetime.now()
        )
        
        # Agregar a la sesión y guardar
        session.add(nuevo_usuario)
        session.commit()
        
        print(f"Usuario '{nombre_usuario}' creado exitosamente con correo '{correo}'")
        return True
    
    except Exception as e:
        session.rollback()
        print(f"Error al crear usuario: {e}")
        return False
    
    finally:
        session.close()

# Ejecutar el script si se llama directamente
if __name__ == "__main__":
    # Datos del usuario a insertar
    NOMBRE_USUARIO = "AlexisLzL"
    CORREO = "elpatriarcadoviva@gmail.com"
    CONTRASENA = "Dork0909"
    ROL = "admin"  # Puedes cambiar a "admin" si es necesario
    
    # Insertar el usuario
    resultado = insertar_usuario(NOMBRE_USUARIO, CORREO, CONTRASENA, ROL)
    
    if resultado:
        print("\nPuedes verificar la creación del usuario ejecutando el script 'verificar_tablas.py'")
    else:
        print("\nNo se pudo crear el usuario. Verifica los logs para más información.")