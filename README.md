Proyecto MAX30101 - Registro y Clasificación de Señales PPG

Este proyecto usa el sensor MAX30101 junto con un Arduino y un script en
Python para registrar señales PPG en tiempo real (RED, IR y GREEN) y
clasificarlas en diferentes momentos (Clase 1, Clase 2, Clase 3).

Requisitos Hardware

-   Sensor MAX30101
-   Arduino (UNO, Nano, etc.)
-   Cable USB y cables dupont

Software

-   Arduino IDE con la librería SparkFun MAX3010x
-   Python 3.x con librerías:
    -   pyserial
    -   pandas
    -   matplotlib
    -   keyboard

Instalación de librerías en Python:

pip install pyserial pandas matplotlib keyboard

Funcionamiento

1.  Conectar el MAX30101 al Arduino por I2C (SDA, SCL).
2.  Cargar el código de Arduino que envía: Tiempo[ms], RED, IR, GREEN
3.  Ejecutar el script en Python (max30101_logger.py).
4.  Durante la ejecución:
    -   Presiona 1, 2 o 3 para etiquetar el segmento de señal.
    -   Presiona ESPACIO para detener la captura.
5.  Al finalizar, se guardan:
    -   Un archivo .csv con todos los datos y su clase.
    -   Una imagen .png con la gráfica de las señales y las clases.

Archivos Generados

-   max30101_datos_YYYYMMDD_HHMMSS.csv → Datos crudos con etiqueta de
    clase.
-   max30101_datos_YYYYMMDD_HHMMSS.png → Gráfica de PPG y clases.
