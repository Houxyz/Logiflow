# Script principal para inicializar el banco de datos legales y normativos
import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar módulos necesarios
from database_lzl.models_sqlalchemy import create_tables
from database_lzl.inicializar_datos import inicializar_categorias_normativas
from database_lzl.inicializar_tarifas import inicializar_tarifas_ligie

def inicializar_banco_datos():
    """
    Función principal para inicializar el banco de datos legales y normativos.
    Crea las tablas y carga los datos iniciales.
    """
    print("=== INICIALIZACIÓN DEL BANCO DE DATOS LEGALES Y NORMATIVOS ===")
    print("\n1. Creando tablas en la base de datos...")
    create_tables()
    
    print("\n2. Inicializando categorías normativas...")
    inicializar_categorias_normativas()
    
    print("\n3. Inicializando tarifas LIGIE de ejemplo...")
    inicializar_tarifas_ligie()
    
    print("\n=== INICIALIZACIÓN COMPLETADA ===")
    print("El banco de datos legales y normativos ha sido configurado correctamente.")
    print("Puede verificar las tablas creadas ejecutando el script 'verificar_tablas.py'")

if __name__ == "__main__":
    inicializar_banco_datos()