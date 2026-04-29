"""
==============================================================
   CAPTURA SIMPLE DE DATOS MAX30101 / MAX30102
   (SOLO DATA CRUDA)
==============================================================

¿QUÉ HACE ESTE PROGRAMA?
--------------------------------------------------------------

Este script:

1. Lee datos enviados por Arduino
2. Recibe señales:
      - RED
      - IR
      - GREEN
3. Guarda datos en CSV
4. NO usa etiquetas
5. NO genera gráficas

==============================================================
   ¿CUÁNDO USAR ESTA VERSIÓN?
==============================================================

Usar esta versión cuando:

 Solo quieres guardar datos
 No necesitas etiquetar
 No necesitas gráficas
 Quieres máxima velocidad
 Deseas procesamiento posterior

==============================================================
   REQUISITOS
==============================================================

Instalar librerías:

   pip install pyserial pandas

==============================================================
   LIBRERÍAS UTILIZADAS
==============================================================

serial
   Comunicación serial con Arduino

pandas
   Guardar archivos CSV

time
   Manejo de tiempo

os
   Manejo de carpetas

==============================================================
   IMPORTANTE SOBRE EL SERIAL
==============================================================

Arduino debe enviar:

Tiempo[ms],RED,IR,GREEN

Ejemplo:

1200,51234,62000,1500

==============================================================
   PUERTO COM
==============================================================

Verificar en:

Arduino IDE → Herramientas → Puerto

Ejemplo:

COM5

==============================================================
   BAUDRATE
==============================================================

Debe coincidir EXACTAMENTE con Arduino.

Si Arduino tiene:

Serial.begin(115200);

Aquí también debe ser:

BAUD = 115200

==============================================================
   FINALIZAR PROGRAMA
==============================================================

Presionar:

CTRL + C

==============================================================
"""


# ==========================================================
# IMPORTAR LIBRERÍAS
# ==========================================================

import serial
import pandas as pd
import time
import os


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

# ----------------------------------------------------------
# PUERTO COM
# ----------------------------------------------------------
#
# Verificar en:
#
# Arduino IDE → Herramientas → Puerto
# ----------------------------------------------------------

PORT = "COM5"


# ----------------------------------------------------------
# BAUDRATE
# ----------------------------------------------------------
#
# Debe coincidir con Arduino
# ----------------------------------------------------------

BAUD = 115200


# ==========================================================
# CARPETA DE SALIDA
# ==========================================================

# CAMBIAR SEGÚN SU COMPUTADORA

OUTPUT_DIR = r"D:\Datos_MAX30101"


# Crear carpeta automáticamente
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================================
# CREAR NOMBRE AUTOMÁTICO
# ==========================================================

timestamp = time.strftime("%Y%m%d_%H%M%S")

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    f"max30101_raw_{timestamp}.csv"
)


# ==========================================================
# INICIAR SERIAL
# ==========================================================

print("==============================================")
print("Inicializando comunicación serial...")
print("==============================================")


# Abrir puerto serial
ser = serial.Serial(PORT, BAUD, timeout=1)


# Esperar reinicio Arduino
time.sleep(2)

print("Conexión serial establecida.")
print()

print("==============================================")
print("CAPTURANDO DATOS...")
print("Presione CTRL + C para finalizar")
print("==============================================")


# ==========================================================
# LISTA PARA GUARDAR DATOS
# ==========================================================

data = []


# ==========================================================
# LOOP PRINCIPAL
# ==========================================================

try:

    while True:

        # ==================================================
        # LEER LÍNEA DEL SERIAL
        # ==================================================

        line = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()


        # Ignorar encabezado CSV
        if line and not line.startswith("Tiempo"):

            try:

                # ==============================================
                # SEPARAR CSV
                # ==============================================

                valores = line.split(",")


                # Verificar columnas correctas
                if len(valores) == 4:

                    # Extraer variables
                    t, red, ir, green = valores


                    # ==========================================
                    # CONVERTIR A NÚMEROS
                    # ==========================================

                    t = int(t)

                    red = float(red)
                    ir = float(ir)
                    green = float(green)


                    # ==========================================
                    # GUARDAR DATOS
                    # ==========================================

                    data.append([
                        t,
                        red,
                        ir,
                        green
                    ])


                    # ==========================================
                    # MOSTRAR EN TERMINAL
                    # ==========================================

                    print(
                        f"T={t} ms | "
                        f"RED={red:.0f} | "
                        f"IR={ir:.0f} | "
                        f"GREEN={green:.0f}"
                    )

            except Exception as e:

                print(f"Error de lectura: {e}")


# ==========================================================
# DETENER CON CTRL + C
# ==========================================================

except KeyboardInterrupt:

    print()
    print("Captura detenida por el usuario.")


# ==========================================================
# CERRAR SERIAL
# ==========================================================

ser.close()

print("Puerto serial cerrado.")


# ==========================================================
# CREAR DATAFRAME
# ==========================================================

df = pd.DataFrame(
    data,
    columns=[
        "Tiempo[ms]",
        "RED",
        "IR",
        "GREEN"
    ]
)


# ==========================================================
# GUARDAR CSV
# ==========================================================

df.to_csv(OUTPUT_FILE, index=False)

print()
print("==============================================")
print("CSV GUARDADO CORRECTAMENTE")
print("==============================================")
print(OUTPUT_FILE)


# ==========================================================
# RESUMEN FINAL
# ==========================================================

print()
print("==============================================")
print("RESUMEN")
print("==============================================")
print(f"Muestras capturadas: {len(df)}")
print(f"Archivo CSV: {OUTPUT_FILE}")
print("==============================================")
