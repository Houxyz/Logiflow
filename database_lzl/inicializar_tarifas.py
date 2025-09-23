# Script para inicializar datos de tarifas LIGIE en la base de datos
from sqlalchemy.exc import IntegrityError
from database_lzl.models_sqlalchemy import get_session, TarifaLIGIE
from datetime import date

def inicializar_tarifas_ligie():
    """
    Inicializa algunas tarifas LIGIE de ejemplo en la base de datos.
    """
    # Lista de tarifas LIGIE de ejemplo (versión 2022)
    tarifas = [
        {
            "fraccion_arancelaria": "0101.21.01",
            "descripcion": "Caballos reproductores de raza pura.",
            "unidad_medida": "Cabeza",
            "arancel_general": "Ex.",
            "version_tarifa": "2022",
            "fecha_vigencia": date(2022, 1, 1),
            "notas": "Fracción arancelaria vigente desde 2022"
        },
        {
            "fraccion_arancelaria": "8471.30.01",
            "descripcion": "Máquinas automáticas para tratamiento o procesamiento de datos, portátiles, de peso inferior o igual a 10 kg, que estén constituidas, al menos, por una unidad central de proceso, un teclado y un visualizador.",
            "unidad_medida": "Pieza",
            "arancel_general": "Ex.",
            "version_tarifa": "2022",
            "fecha_vigencia": date(2022, 1, 1),
            "notas": "Fracción arancelaria vigente desde 2022"
        },
        {
            "fraccion_arancelaria": "8703.22.01",
            "descripcion": "De cilindrada superior a 1,000 cm³ pero inferior o igual a 1,500 cm³.",
            "unidad_medida": "Pieza",
            "arancel_general": "20",
            "version_tarifa": "2022",
            "fecha_vigencia": date(2022, 1, 1),
            "notas": "Fracción arancelaria vigente desde 2022"
        },
        # Versión histórica 2020
        {
            "fraccion_arancelaria": "8703.22.01",
            "descripcion": "De cilindrada superior a 1,000 cm³ pero inferior o igual a 1,500 cm³.",
            "unidad_medida": "Pieza",
            "arancel_general": "20",
            "version_tarifa": "2020",
            "fecha_vigencia": date(2020, 1, 1),
            "notas": "Fracción arancelaria versión 2020"
        },
        # Versión histórica 2007
        {
            "fraccion_arancelaria": "8703.22.01",
            "descripcion": "De cilindrada superior a 1,000 cm³ pero inferior o igual a 1,500 cm³.",
            "unidad_medida": "Pieza",
            "arancel_general": "30",
            "version_tarifa": "2007",
            "fecha_vigencia": date(2007, 1, 1),
            "notas": "Fracción arancelaria versión 2007"
        }
    ]
    
    # Obtener sesión
    session = get_session()
    
    try:
        # Insertar tarifas
        for tarifa in tarifas:
            # Verificar si ya existe
            existe = session.query(TarifaLIGIE).filter_by(
                fraccion_arancelaria=tarifa["fraccion_arancelaria"],
                version_tarifa=tarifa["version_tarifa"]
            ).first()
            
            if not existe:
                nueva_tarifa = TarifaLIGIE(
                    fraccion_arancelaria=tarifa["fraccion_arancelaria"],
                    descripcion=tarifa["descripcion"],
                    unidad_medida=tarifa["unidad_medida"],
                    arancel_general=tarifa["arancel_general"],
                    version_tarifa=tarifa["version_tarifa"],
                    fecha_vigencia=tarifa["fecha_vigencia"],
                    notas=tarifa["notas"]
                )
                session.add(nueva_tarifa)
                print(f"Tarifa agregada: {tarifa['fraccion_arancelaria']} (versión {tarifa['version_tarifa']})")
            else:
                print(f"La tarifa '{tarifa['fraccion_arancelaria']}' (versión {tarifa['version_tarifa']}) ya existe.")
        
        # Confirmar cambios
        session.commit()
        print("Inicialización de tarifas LIGIE completada.")
    except IntegrityError as e:
        session.rollback()
        print(f"Error de integridad: {e}")
    except Exception as e:
        session.rollback()
        print(f"Error al inicializar tarifas: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    inicializar_tarifas_ligie()
    print("Proceso de inicialización de tarifas LIGIE completado.")