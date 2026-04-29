"""
==============================================================
   CAPTURA Y ETIQUETADO DE DATOS MAX30101 / MAX30102
==============================================================

¿QUÉ HACE ESTE PROGRAMA?
--------------------------------------------------------------

Este script:

1. Lee datos enviados por Arduino
2. Recibe señales ópticas:
      - RED
      - IR
      - GREEN
3. Permite etiquetar datos en tiempo real
4. Grafica señales PPG
5. Guarda datos en CSV
6. Guarda figura PNG automáticamente

==============================================================
   ¿PARA QUÉ SIRVE?
==============================================================

Aplicaciones comunes:

 Fotopletismografía (PPG)
 Frecuencia cardíaca
 SpO2
 Clasificación de estados fisiológicos
 Machine Learning biomédico
 Captura de datasets

==============================================================
   REQUISITOS
==============================================================

Instalar librerías:

   pip install pyserial pandas matplotlib keyboard

==============================================================
   LIBRERÍAS UTILIZADAS
==============================================================

serial
   Comunicación serial con Arduino

pandas
   Guardar CSV fácilmente

time
   Manejo de tiempo

os
   Manejo de carpetas y archivos

keyboard
   Detectar teclas del teclado

matplotlib
   Graficar señales en tiempo real

==============================================================
   IMPORTANTE SOBRE EL SERIAL
==============================================================

El Arduino debe enviar datos CSV así:

Tiempo[ms],RED,IR,GREEN

Ejemplo:

1200,51234,62000,1500

==============================================================
   IMPORTANTE SOBRE EL PUERTO COM
==============================================================

Verificar en Arduino IDE:

   Herramientas → Puerto

Ejemplos:

   COM3
   COM5
   COM8

==============================================================
   IMPORTANTE SOBRE LOS BAUDIOS
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
   EJEMPLO DE ETIQUETAS
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
import matplotlib.pyplot as plt


# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

# ----------------------------------------------------------
# PUERTO COM
# ----------------------------------------------------------
#
# Verificar en:
#
# Arduino IDE → Herramientas → Puerto
#
# CAMBIAR SEGÚN SU PC
# ----------------------------------------------------------

PORT = "COM5"


# ----------------------------------------------------------
# BAUDRATE
# ----------------------------------------------------------
#
# Debe coincidir con Arduino.
#
# Ejemplo en Arduino:
#
# Serial.begin(115200);
# ----------------------------------------------------------

BAUD = 115200


# ==========================================================
# CARPETA DE SALIDA
# ==========================================================

# ----------------------------------------------------------
# Ruta donde se guardarán:
#
# - CSV
# - imágenes PNG
#
# CAMBIAR SEGÚN SU COMPUTADORA
# ----------------------------------------------------------

OUTPUT_DIR = r"D:\Datos_MAX30101"


# Crear carpeta automáticamente si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================================
# CREAR NOMBRE AUTOMÁTICO
# ==========================================================

# Timestamp:
# fecha y hora actual

timestamp = time.strftime("%Y%m%d_%H%M%S")


# Crear nombre único automáticamente
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    f"max30101_datos_{timestamp}.csv"
)


# ==========================================================
# INICIAR COMUNICACIÓN SERIAL
# ==========================================================

print("==============================================")
print("Inicializando comunicación serial...")
print("==============================================")


# Abrir puerto serial
ser = serial.Serial(PORT, BAUD, timeout=1)


# Esperar reinicio de Arduino
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

# Lista donde se almacenarán TODOS los datos
data = []


# Clase inicial
current_class = "Clase 1"


# Valor numérico de clase
# útil para graficar
class_numeric = 1


# Guardar posiciones donde cambia la clase
class_lines = []


# ==========================================================
# CONFIGURAR GRÁFICAS
# ==========================================================

# Activar modo interactivo
plt.ion()


# Crear 2 gráficas:
#
# ax1 -> señales PPG
# ax2 -> etiquetas/clases

fig, (ax1, ax2) = plt.subplots(
    2,
    1,
    figsize=(10, 7),
    sharex=True,
    gridspec_kw={'height_ratios': [3, 1]}
)


# ----------------------------------------------------------
# GRÁFICA SUPERIOR
# ----------------------------------------------------------

ax1.set_title("PPG en tiempo real (RED, IR, GREEN)")
ax1.set_ylabel("Intensidad (u.a.)")


# ----------------------------------------------------------
# GRÁFICA INFERIOR
# ----------------------------------------------------------

ax2.set_title("Clase en el tiempo")
ax2.set_xlabel("Muestras")
ax2.set_ylabel("Clase")

ax2.set_yticks([1, 2, 3])

ax2.set_yticklabels([
    "Clase 1",
    "Clase 2",
    "Clase 3"
])


# ==========================================================
# VECTORES PARA GRAFICAR
# ==========================================================

# x_vals:
# eje horizontal (número de muestra)

x_vals = []

# señales ópticas
red_vals = []
ir_vals = []
green_vals = []

# clases
class_vals = []


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

        print("Captura finalizada por el usuario.")
        break


    # ------------------------------------------------------
    # CAMBIAR A CLASE 1
    # ------------------------------------------------------

    elif keyboard.is_pressed("1"):

        current_class = "Clase 1"
        class_numeric = 1

        print("Clase cambiada a 1")

        # Guardar posición del cambio
        class_lines.append(len(x_vals))

        # Evitar múltiples detecciones
        time.sleep(0.3)


    # ------------------------------------------------------
    # CAMBIAR A CLASE 2
    # ------------------------------------------------------

    elif keyboard.is_pressed("2"):

        current_class = "Clase 2"
        class_numeric = 2

        print("Clase cambiada a 2")

        class_lines.append(len(x_vals))

        time.sleep(0.3)


    # ------------------------------------------------------
    # CAMBIAR A CLASE 3
    # ------------------------------------------------------

    elif keyboard.is_pressed("3"):

        current_class = "Clase 3"
        class_numeric = 3

        print("Clase cambiada a 3")

        class_lines.append(len(x_vals))

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


            # Verificar número correcto de columnas
            if len(valores) == 4:

                # Extraer variables
                t, red, ir, green = valores


                # ==================================================
                # CONVERTIR A NÚMEROS
                # ==================================================

                red = float(red)
                ir = float(ir)
                green = float(green)


                # ==================================================
                # GUARDAR DATOS
                # ==================================================

                data.append([
                    int(t),
                    red,
                    ir,
                    green,
                    current_class
                ])


                # ==================================================
                # ACTUALIZAR VECTORES
                # ==================================================

                x_vals.append(len(x_vals))

                red_vals.append(red)
                ir_vals.append(ir)
                green_vals.append(green)

                class_vals.append(class_numeric)


                # ==================================================
                # ACTUALIZAR GRÁFICA SUPERIOR
                # ==================================================

                ax1.clear()

                ax1.plot(
                    x_vals,
                    red_vals,
                    label="RED"
                )

                ax1.plot(
                    x_vals,
                    ir_vals,
                    label="IR"
                )

                ax1.plot(
                    x_vals,
                    green_vals,
                    label="GREEN"
                )


                # Dibujar líneas verticales
                # donde cambia la clase
                for c in class_lines:

                    ax1.axvline(
                        c,
                        color="red",
                        linestyle="--"
                    )


                ax1.set_ylabel("Intensidad (u.a.)")

                ax1.set_title(
                    f"PPG - Clase actual: {current_class}"
                )

                ax1.legend()


                # ==================================================
                # ACTUALIZAR GRÁFICA INFERIOR
                # ==================================================

                ax2.clear()

                ax2.step(
                    x_vals,
                    class_vals,
                    where="post",
                    color="black"
                )


                # Dibujar cambios de clase
                for c in class_lines:

                    ax2.axvline(
                        c,
                        color="red",
                        linestyle="--"
                    )


                ax2.set_yticks([1, 2, 3])

                ax2.set_yticklabels([
                    "Clase 1",
                    "Clase 2",
                    "Clase 3"
                ])

                ax2.set_xlabel("Muestras")
                ax2.set_ylabel("Clase")


                # ==================================================
                # ACTUALIZAR VENTANA
                # ==================================================

                plt.pause(0.01)

        except Exception as e:

            # Mostrar error sin detener programa
            print(f"Error de lectura: {e}")


# ==========================================================
# CERRAR SERIAL
# ==========================================================

ser.close()

print("Puerto serial cerrado.")


# ==========================================================
# CONVERTIR A DATAFRAME
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
# GUARDAR FIGURA
# ==========================================================

# Cambiar extensión .csv → .png
FIG_FILE = os.path.splitext(OUTPUT_FILE)[0] + ".png"


# Desactivar modo interactivo
plt.ioff()


# Guardar imagen
fig.savefig(FIG_FILE, dpi=300)

print()
print("Figura guardada:")
print(FIG_FILE)


# ==========================================================
# MOSTRAR GRÁFICA FINAL
# ==========================================================

plt.show()


# ==========================================================
# RESUMEN FINAL
# ==========================================================

print()
print("==============================================")
print("RESUMEN")
print("==============================================")
print(f"Muestras capturadas: {len(df)}")
print(f"CSV: {OUTPUT_FILE}")
print(f"PNG: {FIG_FILE}")
print("==============================================")
