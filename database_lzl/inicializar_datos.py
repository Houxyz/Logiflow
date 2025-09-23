# Script para inicializar datos básicos en la base de datos
from sqlalchemy.exc import IntegrityError
from database_lzl.models_sqlalchemy import get_session, create_tables, CategoriaNormativa

def inicializar_categorias_normativas():
    """
    Inicializa las categorías normativas básicas en la base de datos.
    """
    # Lista de categorías normativas básicas
    categorias = [
        {"nombre": "Tratados de Libre Comercio", "descripcion": "Acuerdos comerciales entre países que eliminan barreras al comercio."},
        {"nombre": "Códigos y Leyes", "descripcion": "Legislación fundamental en materia de comercio exterior."},
        {"nombre": "Reglamentos", "descripcion": "Normas que desarrollan y complementan las leyes."},
        {"nombre": "Decretos", "descripcion": "Disposiciones emitidas por el poder ejecutivo."},
        {"nombre": "Acuerdos", "descripcion": "Disposiciones administrativas en materia de comercio exterior."},
        {"nombre": "Regulaciones y Restricciones no Arancelarias", "descripcion": "Medidas de control al comercio exterior distintas de los aranceles."},
        {"nombre": "INCOTERMS", "descripcion": "Términos internacionales de comercio que definen responsabilidades."},
        {"nombre": "Tarifa de la LIGIE", "descripcion": "Ley de los Impuestos Generales de Importación y Exportación."},
    ]
    
    # Obtener sesión
    session = get_session()
    
    try:
        # Insertar categorías
        for categoria in categorias:
            # Verificar si ya existe
            existe = session.query(CategoriaNormativa).filter_by(nombre=categoria["nombre"]).first()
            if not existe:
                nueva_categoria = CategoriaNormativa(
                    nombre=categoria["nombre"],
                    descripcion=categoria["descripcion"]
                )
                session.add(nueva_categoria)
                print(f"Categoría agregada: {categoria['nombre']}")
            else:
                print(f"La categoría '{categoria['nombre']}' ya existe.")
        
        # Confirmar cambios
        session.commit()
        print("Inicialización de categorías normativas completada.")
    except IntegrityError as e:
        session.rollback()
        print(f"Error de integridad: {e}")
    except Exception as e:
        session.rollback()
        print(f"Error al inicializar categorías: {e}")
    finally:
        session.close()

def inicializar_datos():
    """
    Función principal para inicializar todos los datos básicos.
    """
    # Asegurar que las tablas existan
    create_tables()
    
    # Inicializar categorías normativas
    inicializar_categorias_normativas()
    
    # Aquí se pueden agregar más funciones para inicializar otros datos

if __name__ == "__main__":
    inicializar_datos()
    print("Proceso de inicialización de datos completado.")