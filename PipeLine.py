import csv
import mysql.connector

# ==========================================
# 1. EXTRACCIÓN (Extract)
# ==========================================
# Leemos el archivo CSV con la telemetría de tus motores
archivo_csv = "telemetria_chiller.csv"
datos_crudos = []

try:
    with open(archivo_csv, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            datos_crudos.append(fila)
    print("--- [E] Éxito: Telemetría extraída del CSV ---")
except FileNotFoundError:
    print("❌ Error: No se encontró el archivo telemetria_chiller.csv en esta carpeta.")
    exit()

# ==========================================
# 2. TRANSFORMACIÓN (Transform - Lógica Predictiva)
# ==========================================
datos_procesados = []

for fila in datos_crudos:
    id_motor = fila["id_motor"]
    temp = float(fila["temperatura_c"])
    voltaje = float(fila["voltaje_v"])
    corriente = float(fila["corriente_a"])
    vibracion = float(fila["vibracion_mms"])
    horas = int(fila["horas_operacion"])
    
    # 🚨 REGLAS DE NEGOCIO PARA MANTENIMIENTO PREDICTIVO 4.0
    if temp >= 85.0 and corriente >= 18.0:
        alerta = "CRÍTICO: Fallo Inminente de Rodamientos"
    elif vibracion >= 3.5:
        alerta = "ADVERTENCIA: Alta Vibración / Fatiga Mecánica"
    elif temp >= 75.0:
        alerta = "ADVERTENCIA: Alta Temperatura"
    else:
        alerta = "Normal"
        
    # Guardamos los datos estructurados incluyendo el diagnóstico predictivo
    datos_procesados.append((id_motor, temp, voltaje, corriente, vibracion, horas, alerta))

print("--- [T] Éxito: Datos transformados y Alertas Predictivas calculadas ---")

# ==========================================
# 3. CARGA (Load)
# ==========================================
try:
    # Nos conectamos a tu base de datos local corregida
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789a",  # <-- Dejé tu contraseña aquí de forma segura
        database="v1_pipeline"   # <-- Conectado al nuevo tanque de almacenamiento
    )
    
    cursor = conexion.cursor()
    
    # Consulta SQL para inyectar los datos en tu tabla industrial
    query_insertar = """
        INSERT INTO telemetria_motores 
        (id_motor, temperatura_c, voltaje_v, corriente_a, vibracion_mms, horas_operacion, estado_alerta)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    # Inyección masiva de los sensores de tus dos Chillers
    cursor.executemany(query_insertar, datos_procesados)
    conexion.commit()
    
    print(f"--- [L] ¡Éxito! {cursor.rowcount} registros de telemetría cargados en v1_pipeline ---")

except mysql.connector.Error as error:
    print(f"❌ Error en la carga del pipeline: {error}")

finally:
    if 'conexion' in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("--- Conexión finalizada limpiamente ---")
