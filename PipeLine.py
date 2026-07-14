Python 3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> import mysql.connector
... 
... print("--- [E] Extrayendo datos crudos ---")
... print("--- [T] Transformando datos con Python ---")
... 
... try:
...     conexion = mysql.connector.connect(
...         host="localhost",
...         user="root",
...         password="123456789a",  # clave de MySQL
...         database="mi_primer_pipeline"
...     )
...     print("--- [L] ¡Carga exitosa! Conectado a MySQL ---")
...     conexion.close()
... except Exception as e:
...     print(f"❌ Error de conexión: {e}")
