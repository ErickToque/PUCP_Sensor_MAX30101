/*
==============================================================
   MAX30101 / MAX30102 - CAPTURA DE DATOS EN FORMATO CSV
==============================================================

¿QUÉ HACE ESTE CÓDIGO?
--------------------------------------------------------------

Este programa:

1. Inicializa el sensor MAX30101/MAX30102/MAX3050
2. Lee señales ópticas:
      - RED
      - IR (Infrarrojo)
      - GREEN (Verde)
3. Envía datos por puerto serial
4. Imprime datos en formato CSV

==============================================================
   ¿PARA QUÉ SIRVE?
==============================================================

Este sensor se usa comúnmente para:

 Frecuencia cardíaca
 SpO2 (oxígeno en sangre)
 Fotopletismografía (PPG)
 Biomarcadores fisiológicos
 Señales biomédicas

==============================================================
   LIBRERÍA NECESARIA
==============================================================

 MUY IMPORTANTE

Instalar la librería OFICIAL de SparkFun.

En Arduino IDE:

   Programa → Incluir librería → Administrar bibliotecas

Buscar:

   SparkFun MAX3010x Pulse and Proximity Sensor Library

Autor:

   SparkFun Electronics

--------------------------------------------------------------
 IMPORTANTE
--------------------------------------------------------------

NO usar librerías incompatibles o antiguas.

A veces existen conflictos entre librerías similares.

Si aparecen errores extraños:

1. Cerrar Arduino IDE
2. Ir a:

Windows:
   Documentos/Arduino/libraries

3. Eliminar librerías duplicadas relacionadas con:
   - MAX3010x
   - MAX30105
   - MAX30102

4. Dejar únicamente la oficial de SparkFun

==============================================================
   CONEXIONES I2C
==============================================================

MAX30101/MAX30102 → Arduino UNO

VIN   → 3.3V o 5V (según módulo)
GND   → GND
SCL   → A5
SDA   → A4

--------------------------------------------------------------
ESP32
--------------------------------------------------------------

VIN   → 3.3V
GND   → GND
SCL   → GPIO22
SDA   → GPIO21

==============================================================
   FORMATO DE SALIDA
==============================================================

Tiempo[ms],RED,IR,GREEN

Ejemplo:

1250,51234,62311,1500

==============================================================
   SOBRE LAS UNIDADES
==============================================================

Los valores RED/IR/GREEN:

 NO están en voltios
 NO están en mV

Son valores ADC internos del sensor:

   unidades arbitrarias (u.a.)

==============================================================
   SOBRE EL SAMPLE RATE
==============================================================

sampleRate = 100 Hz

Significa:

100 muestras por segundo

delay(10):

10 ms entre muestras

==============================================================
*/

#include <Wire.h>

/*
==============================================================
   LIBRERÍA PRINCIPAL DEL SENSOR
==============================================================

MAX30105.h funciona tanto para:

- MAX30101
- MAX30102
- MAX30105

porque comparten arquitectura similar.
==============================================================
*/
#include "MAX30105.h"


/*
==============================================================
   LIBRERÍA heartRate.h
==============================================================

Se usa normalmente para:

- frecuencia cardíaca
- cálculo de BPM
- SpO2

 En este ejemplo NO la usamos directamente,
pero se deja incluida para futuras extensiones.
==============================================================
*/
#include "heartRate.h"


// Crear objeto sensor
MAX30105 sensor;


/*
==============================================================
   CONFIGURACIÓN DEL SENSOR
==============================================================
*/


/*
--------------------------------------------------------------
Brillo LED
--------------------------------------------------------------

Rango:

0 - 255

 Valores altos:
- mayor intensidad
- mayor consumo
- posible saturación

50 suele ser un buen inicio.
--------------------------------------------------------------
*/
const byte ledBrightness = 50;


/*
--------------------------------------------------------------
Promedio de muestras
--------------------------------------------------------------

Valores posibles:

1, 2, 4, 8, 16, 32

Mayor promedio:
 menos ruido
 respuesta más lenta
--------------------------------------------------------------
*/
const byte sampleAverage = 4;


/*
--------------------------------------------------------------
Modo LEDs
--------------------------------------------------------------

1 = solo RED
2 = RED + IR
3 = RED + IR + GREEN

 GREEN solo existe en algunos modelos.
--------------------------------------------------------------
*/
const byte ledMode = 3;


/*
--------------------------------------------------------------
Frecuencia de muestreo
--------------------------------------------------------------

100 Hz = 100 muestras/segundo
--------------------------------------------------------------
*/
const int sampleRate = 100;


/*
--------------------------------------------------------------
Ancho de pulso LED
--------------------------------------------------------------

Opciones:

69
118
215
411

Mayor ancho:
 mayor sensibilidad
 mayor consumo
--------------------------------------------------------------
*/
const int pulseWidth = 411;


/*
--------------------------------------------------------------
Rango ADC
--------------------------------------------------------------

Opciones:

2048
4096
8192
16384

Mayor rango:
 evita saturación
 menor resolución fina
--------------------------------------------------------------
*/
const int adcRange = 16384;


/*
==============================================================
   SETUP
==============================================================
*/
void setup() {

  /*
  ------------------------------------------------------------
  Inicializar serial
  ------------------------------------------------------------

  115200 baud:
  velocidad alta para transmitir datos rápidamente
  ------------------------------------------------------------
  */
  Serial.begin(115200);


  /*
  ------------------------------------------------------------
  Inicializar comunicación I2C
  ------------------------------------------------------------
  */
  Wire.begin();


  /*
  ------------------------------------------------------------
  Inicializar sensor
  ------------------------------------------------------------

  I2C_SPEED_STANDARD:
  usa velocidad estándar I2C (100 kHz)

  Más estable para muchos módulos.
  ------------------------------------------------------------
  */
  if (!sensor.begin(Wire, I2C_SPEED_STANDARD)) {

    Serial.println("Error: MAX30101/MAX30102 no detectado.");
    Serial.println("Revisa conexiones SDA/SCL.");
    Serial.println("Revisa alimentación.");
    Serial.println("Revisa librerías.");

    // Detener programa
    while (1);
  }


  /*
  ------------------------------------------------------------
  Configurar sensor
  ------------------------------------------------------------
  */
  sensor.setup(
    ledBrightness,
    sampleAverage,
    ledMode,
    sampleRate,
    pulseWidth,
    adcRange
  );


  /*
  ------------------------------------------------------------
  Encabezado CSV
  ------------------------------------------------------------

  Esto ayuda a Python/Pandas
  a reconocer las columnas.
  ------------------------------------------------------------
  */
  Serial.println("Tiempo[ms],RED (u.a.),IR (u.a.),GREEN (u.a.)");
}


/*
==============================================================
   LOOP PRINCIPAL
==============================================================
*/
void loop() {

  /*
  ------------------------------------------------------------
  Leer señal RED
  ------------------------------------------------------------
  */
  long red = sensor.getRed();


  /*
  ------------------------------------------------------------
  Leer señal infrarroja
  ------------------------------------------------------------
  */
  long ir = sensor.getIR();


  /*
  ------------------------------------------------------------
  Leer señal GREEN
  ------------------------------------------------------------

  Solo si ledMode == 3
  ------------------------------------------------------------
  */
  long green = (ledMode == 3)
               ? sensor.getGreen()
               : 0;


  /*
  ============================================================
     IMPRIMIR DATOS EN FORMATO CSV
  ============================================================

  Formato:

  tiempo,red,ir,green

  Ejemplo:

  1250,51234,62311,1500
  ============================================================
  */

  // Tiempo actual en milisegundos
  Serial.print(millis());
  Serial.print(",");

  // Señal RED
  Serial.print(red);
  Serial.print(",");

  // Señal IR
  Serial.print(ir);
  Serial.print(",");

  // Señal GREEN
  Serial.println(green);


  /*
  ------------------------------------------------------------
  Esperar 10 ms
  ------------------------------------------------------------

  100 Hz ≈ 10 ms entre muestras
  ------------------------------------------------------------
  */
  delay(10);
}
