import serial
import pandas as pd
import time
import os
import keyboard
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
PORT = "COM5" #ACTUALICE CON SU PUERTO, ESO SE AVERIGUA FÁCIL CON ARDUINO IDE
BAUD = 115200 #VERIFIQUE QUE SEAN LOS BAUDIOS CORRECTOS

# Carpeta de salida
OUTPUT_DIR = r"E:\PUCP\Biomecatronica\Sensor_MAX30101\Datos" #ACTUALICE CON SU RUTA ACTUAL
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Nombre de archivo con timestamp
timestamp = time.strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"max30101_datos_{timestamp}.csv")

# --- INICIO SERIAL ---
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

print("Capturando datos del MAX30101...")
print("Presiona '1', '2' o '3' para cambiar de clase. Presiona 'ESPACIO' para terminar.") #IMPORTANTE PARA ETIQUETAR

# --- LISTA DE DATOS ---
data = []
current_class = "Clase 1"
class_numeric = 1
class_lines = []  # marcas cuando cambia de clase

# --- CONFIG PLOTEO ---
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,7), sharex=True,
                               gridspec_kw={'height_ratios':[3,1]})

ax1.set_title("PPG en tiempo real (RED, IR, GREEN)")
ax1.set_ylabel("Intensidad (u.a.)")

ax2.set_title("Clase en el tiempo")
ax2.set_xlabel("Muestras")
ax2.set_ylabel("Clase")
ax2.set_yticks([1,2,3])
ax2.set_yticklabels(["Clase 1","Clase 2","Clase 3"])

# --- VECTORES ---
x_vals, red_vals, ir_vals, green_vals, class_vals = [], [], [], [], []

# --- LOOP ---
while True:
    if keyboard.is_pressed("space"):  # terminar
        print("Captura finalizada por el usuario.")
        break
    elif keyboard.is_pressed("1"):
        current_class = "Clase 1"; class_numeric = 1
        print("Clase cambiada a 1")
        class_lines.append(len(x_vals)); time.sleep(0.3)
    elif keyboard.is_pressed("2"):
        current_class = "Clase 2"; class_numeric = 2
        print("Clase cambiada a 2")
        class_lines.append(len(x_vals)); time.sleep(0.3)
    elif keyboard.is_pressed("3"):
        current_class = "Clase 3"; class_numeric = 3
        print("Clase cambiada a 3")
        class_lines.append(len(x_vals)); time.sleep(0.3)

    line = ser.readline().decode("utf-8", errors="ignore").strip()
    if line and not line.startswith("Tiempo"):
        try:
            valores = line.split(",")
            if len(valores) == 4:  # Tiempo, RED, IR, GREEN
                t, red, ir, green = valores
                red, ir, green = float(red), float(ir), float(green)

                # Guardar en lista
                data.append([int(t), red, ir, green, current_class])

                # --- actualizar vectores ---
                x_vals.append(len(x_vals))
                red_vals.append(red)
                ir_vals.append(ir)
                green_vals.append(green)
                class_vals.append(class_numeric)

                # --- actualizar gráfica ---
                ax1.clear()
                ax1.plot(x_vals, red_vals, label="RED")
                ax1.plot(x_vals, ir_vals, label="IR")
                ax1.plot(x_vals, green_vals, label="GREEN")

                for c in class_lines:
                    ax1.axvline(c, color="red", linestyle="--")
                ax1.set_ylabel("Intensidad (u.a.)")
                ax1.set_title(f"PPG - Clase actual: {current_class}")
                ax1.legend()

                ax2.clear()
                ax2.step(x_vals, class_vals, where="post", color="black")
                for c in class_lines:
                    ax2.axvline(c, color="red", linestyle="--")
                ax2.set_yticks([1,2,3])
                ax2.set_yticklabels(["Clase 1","Clase 2","Clase 3"])
                ax2.set_xlabel("Muestras")
                ax2.set_ylabel("Clase")

                plt.pause(0.01)
        except:
            pass

ser.close()

# --- CONVERTIR A DATAFRAME ---
df = pd.DataFrame(data, columns=["Tiempo[ms]", "RED", "IR", "GREEN", "Clase"])

# --- GUARDAR CSV ---
df.to_csv(OUTPUT_FILE, index=False)
print(f"Datos guardados en {OUTPUT_FILE}")

# --- GUARDAR FIGURA ---
FIG_FILE = os.path.splitext(OUTPUT_FILE)[0] + ".png"
plt.ioff()
fig.savefig(FIG_FILE, dpi=300)
print(f"Figura guardada en {FIG_FILE}")

plt.show()
 
