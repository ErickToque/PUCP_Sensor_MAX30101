"""
==============================================================
   CAPTURA Y ETIQUETADO MAX30101/MAX30102
   (SIN GRÁFICAS EN TIEMPO REAL)
==============================================================

¿QUÉ HACE ESTE PROGRAMA?
--------------------------------------------------------------

Este script:

1. Lee datos enviados por Arduino
2. Recibe señales:
      - RED
      - IR
      - GREEN
3. Permite etiquetar datos usando teclado
4. Guarda datos en CSV
5. NO genera gráficas

==============================================================
   ¿CUÁNDO USAR ESTA VERSIÓN?
==============================================================

Usar esta versión cuando:

 Solo quieres capturar datos
 No necesitas visualizar señales
 Quieres máxima velocidad
 El gráfico en tiempo real consume recursos
 Vas a procesar datos después

==============================================================
   REQUISITOS
==============================================================

Instalar librerías:

   pip install pyserial pandas keyboard

==============================================================
   LIBRERÍAS USADAS
==============================================================

serial
   Comunicación serial con Arduino

pandas
   Guardar CSV

time
   Manejo de tiempo

os
   Manejo de carpetas

keyboard
   Detectar teclas

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

Aquí debe ser:

BAUD = 115200

==============================================================
   CONTROLES
==============================================================

1 -> Clase 1
2 -> Clase 2
3 -> Clase 3

ESPACIO -> finalizar captura

==============================================================
   EJEMPLO DE CLASES
==============================================================

Clase 1 -> reposo
Clase 2 -> ejercicio
Clase 3 -> recuperación

==============================================================
"""


# ==========================================================
# IMPORTAR LIBRERÍAS
# ==========================================================

import serial
import pandas as pd
import time
import os
import keyboard


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
    f"max30101_datos_{timestamp}.csv"
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
print("CONTROLES")
print("==============================================")
print("1 -> Clase 1")
print("2 -> Clase 2")
print("3 -> Clase 3")
print("ESPACIO -> terminar")
print("==============================================")


# ==========================================================
# VARIABLES PRINCIPALES
# ==========================================================

# Lista donde se almacenarán todos los datos
data = []


# Clase inicial
current_class = "Clase 1"


# ==========================================================
# LOOP PRINCIPAL
# ==========================================================

while True:

    # ======================================================
    # DETECTAR TECLAS
    # ======================================================

    # ------------------------------------------------------
    # TERMINAR PROGRAMA
    # ------------------------------------------------------

    if keyboard.is_pressed("space"):

        print()
        print("Captura finalizada por el usuario.")
        break


    # ------------------------------------------------------
    # CLASE 1
    # ------------------------------------------------------

    elif keyboard.is_pressed("1"):

        current_class = "Clase 1"

        print("Clase cambiada a 1")

        # Evitar múltiples detecciones
        time.sleep(0.3)


    # ------------------------------------------------------
    # CLASE 2
    # ------------------------------------------------------

    elif keyboard.is_pressed("2"):

        current_class = "Clase 2"

        print("Clase cambiada a 2")

        time.sleep(0.3)


    # ------------------------------------------------------
    # CLASE 3
    # ------------------------------------------------------

    elif keyboard.is_pressed("3"):

        current_class = "Clase 3"

        print("Clase cambiada a 3")

        time.sleep(0.3)


    # ======================================================
    # LEER DATOS DEL SERIAL
    # ======================================================

    line = ser.readline().decode(
        "utf-8",
        errors="ignore"
    ).strip()


    # Ignorar encabezado CSV
    if line and not line.startswith("Tiempo"):

        try:

            # ==================================================
            # SEPARAR DATOS CSV
            # ==================================================

            valores = line.split(",")


            # Verificar columnas correctas
            if len(valores) == 4:

                # Extraer variables
                t, red, ir, green = valores


                # ==================================================
                # CONVERTIR A NÚMEROS
                # ==================================================

                t = int(t)

                red = float(red)
                ir = float(ir)
                green = float(green)


                # ==================================================
                # GUARDAR DATOS
                # ==================================================

                data.append([
                    t,
                    red,
                    ir,
                    green,
                    current_class
                ])


                # ==================================================
                # MOSTRAR EN TERMINAL
                # ==================================================
                #
                # Puede comentarse para mayor velocidad
                # ==================================================

                print(
                    f"T={t} ms | "
                    f"RED={red:.0f} | "
                    f"IR={ir:.0f} | "
                    f"GREEN={green:.0f} | "
                    f"{current_class}"
                )

        except Exception as e:

            print(f"Error de lectura: {e}")


# ==========================================================
# CERRAR SERIAL
# ==========================================================

ser.close()

print()
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
        "GREEN",
        "Clase"
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
