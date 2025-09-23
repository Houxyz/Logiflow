# Script para verificar la existencia de un usuario específico en la base de datos
import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar módulos necesarios
from database_lzl.models_sqlalchemy import Usuario, get_session

def verificar_usuario(nombre_usuario=None, correo=None):
    """
    Verifica si existe un usuario con el nombre de usuario o correo especificado.
    
    Args:
        nombre_usuario (str, optional): Nombre de usuario a buscar
        correo (str, optional): Correo electrónico a buscar
    """
    if not nombre_usuario and not correo:
        print("Error: Debe proporcionar un nombre de usuario o correo para buscar")
        return
    
    # Crear una sesión de base de datos
    session = get_session()
    
    try:
        # Construir la consulta
        query = session.query(Usuario)
        
        if nombre_usuario:
            query = query.filter(Usuario.nombre_usuario == nombre_usuario)
        
        if correo:
            query = query.filter(Usuario.correo == correo)
        
        # Ejecutar la consulta
        usuario = query.first()
        
        if usuario:
            print("\nUsuario encontrado:")
            print(f"ID: {usuario.id_usuario}")
            print(f"Nombre de usuario: {usuario.nombre_usuario}")
            print(f"Correo: {usuario.correo}")
            print(f"Rol: {usuario.rol}")
            print(f"Activo: {usuario.activo}")
            print(f"Fecha de creación: {usuario.fecha_creacion}")
        else:
            print(f"\nNo se encontró ningún usuario con los criterios especificados")
    
    except Exception as e:
        print(f"Error al buscar usuario: {e}")
    
    finally:
        session.close()

# Ejecutar el script si se llama directamente
if __name__ == "__main__":
    # Buscar el usuario que acabamos de crear
    print("Verificando usuario 'AlexisLzL'...")
    verificar_usuario(nombre_usuario="Dork0909")
    
    print("\nVerificando usuario con correo 'elpatriarcadoviva@gmail.com'...")
    verificar_usuario(correo="elpatriarcadoviva@gmail.com")