# Script para verificar las tablas creadas en la base de datos
from sqlalchemy import inspect
from database_lzl.models_sqlalchemy import get_engine, Usuario, CategoriaNormativa, DocumentoNormativo, ReferenciaDocumento, TarifaLIGIE, Incoterm, Complemento

# Obtener el motor de conexión
engine = get_engine()

# Crear un inspector
inspector = inspect(engine)

# Obtener todas las tablas en la base de datos
tablas = inspector.get_table_names()
print("Tablas en la base de datos:")
for tabla in tablas:
    print(f"- {tabla}")

# Lista de tablas a verificar
tablas_a_verificar = {
    'usuarios': 'Usuario',
    'categorias_normativas': 'Categoría Normativa',
    'documentos_normativos': 'Documento Normativo',
    'referencias_documentos': 'Referencia entre Documentos',
    'tarifas_ligie': 'Tarifa LIGIE',
    'incoterms': 'Incoterm',
    'complementos': 'Complemento'
}

# Verificar cada tabla
for nombre_tabla, descripcion in tablas_a_verificar.items():
    if nombre_tabla in tablas:
        print(f"\nLa tabla '{nombre_tabla}' ({descripcion}) se ha creado correctamente.")
        
        # Mostrar las columnas de la tabla
        print(f"\nColumnas de la tabla '{nombre_tabla}':")
        columnas = inspector.get_columns(nombre_tabla)
        for columna in columnas:
            print(f"- {columna['name']} ({columna['type']})")
    else:
        print(f"\nLa tabla '{nombre_tabla}' ({descripcion}) no se ha creado.")