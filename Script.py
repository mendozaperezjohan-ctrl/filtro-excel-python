import logging
from pathlib import Path
import pandas as pd
# Configuración del logger para mostrar mensajes formateados con hora, nivel de gravedad y mensaje.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'  # Formato de la fecha y hora
)

def filtrar_clientes_peru(
    archivo_origen: str = 'datos_clientes.xlsx',
    archivo_destino: str = 'clientes_peru.xlsx',
    columna_filtro: str = 'Pais',
    pais_objetivo: str = 'Peru'
)  bool:
    """
    Función para leer, validar, limpiar y filtrar datos de un archivo Excel de clientes.
    """ 
    # Convertimos las cadenas de texto a objetos Path de pathlib para garantizar compatibilidad de SO
    ruta_entrada = Path(archivo_origen)
    ruta_salida = Path(archivo_destino)
    # Validamos preventivamente si el archivo de origen existe antes de intentar leerlo
    if not ruta_entrada.exists():
        logging.error(f"El archivo especificado no existe en la ruta: '{ruta_entrada.resolve()}'")
        return False

    try:  # Bloque de control de excepciones para operaciones de lectura o escritura
        logging.info(f"Iniciando lectura del archivo: '{ruta_entrada.name}'")
        
        # Leemos el archivo Excel especificando 'openpyxl' como motor de lectura
        df = pd.read_excel(ruta_entrada, engine='openpyxl')

        # Verificamos que la columna objetivo exista dentro de la estructura cargada
        if columna_filtro not in df.columns:
            logging.error(f"La columna '{columna_filtro}' no fue encontrada. Columnas disponibles: {list(df.columns)}")
            return False

        logging.info(f"Archivo cargado exitosamente. Registros totales procesados: {len(df)}")

        # Convertimos la columna a texto, eliminamos espacios, quitamos tildes y convertimos a minúsculas
        columna_limpia = (
            df[columna_filtro]
            .astype(str)
            .str.strip()
            .str.lower()
            .str.normalize('NFKD')
            .str.encode('ascii', errors='ignore')
            .str.decode('utf-8')
        )

        # Aplicamos la misma normalización al término de búsqueda objetivo
        target_normalizado = (
            pais_objetivo
            .strip()
            .lower()
        )

        # Creamos una mascara booleana comparando la versión limpia de la columna con el objetivo
        mascara_filtro = columna_limpia == target_normalizad
        
        # Filtramos el DataFrame original manteniendo la estructura e información intactas
        df_filtrado = df[mascara_filtro].copy()
        total_encontrados = len(df_filtrado)
        logging.info(f"Registros encontrados para '{pais_objetivo}': {total_encontrados}")

        # Emitimos una advertencia si no se encontró ningún registro
        if total_encontrados == 0:
            logging.warning("El proceso finalizó pero no se encontraron filas que coincidan con el filtro.")

        logging.info(f"Escribiendo resultado en el archivo: '{ruta_salida.name}'")
      
        # Guardamos los datos filtrados en la ruta destino omitiendo la columna de índices autogenerada
        df_filtrado.to_excel(ruta_salida, index=False, engine='openpyxl'

        logging.info(" Proceso completado con éxito.")
        return True

    except ModuleNotFoundError as e:
        logging.critical(f"Falta una dependencia requerida: {e}. Ejecuta 'pip install pandas openpyxl'") 
        return False 
    except Exception as e: 
        logging.error(f"Se produjo un error inesperado durante la ejecución: {e}", exc_info=True)
        return False 

# Punto de entrada estándar en programas de Python
if __name__ == '__main__': 
    filtrar_clientes_peru() 
