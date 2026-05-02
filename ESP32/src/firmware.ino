/*
 * Sistema de Adquisición de Datos RLC de Alta Velocidad
 * Pulso de excitación: 50ms
 * Tiempo de captura total: 100ms
 * Velocidad de transmisión: 460,800 baudios
 */

#include <Arduino.h>

/// Pines de funcionamiento
#define EXCITACION_PIN 5   /// Pin de señal al mosfet
#define SENSOR_PIN 34      /// pin de señal del circuito

/// parámetros del muestreo
#define MAX_MUESTRAS 35000  /// Cantidad de muestras en RAM
uint16_t bufferDatos[MAX_MUESTRAS];
int muestrasTomadas = 0;

/// Tiempos en uS
const unsigned long DURACION_PULSO = 50000;    // 50 ms
const unsigned long CAPTURA_TOTAL = 100000;    // 100 ms total (50ms ON + 50ms OFF)

void setup() {
  Serial.begin(460800);
  
  /// configurar pin de excitación
  pinMode(EXCITACION_PIN, OUTPUT);
  digitalWrite(EXCITACION_PIN, LOW);
  
  /// configurar ADC a 12 bits
  analogReadResolution(12);
  
  /// Atenuación para rango 0V - 3.3V
  analogSetAttenuation(ADC_11db);

}

void loop() {
  
  /// para esperar comando desde Python
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando == "INICIAR") {
      ejecutarCapturaRLC();
    }
    else if (comando.startsWith("CAPTURAR_ESCALON")) {
      ejecutarCapturaRLC();
    }
  }
}

void ejecutarCapturaRLC() {
  muestrasTomadas = 0;
  bool pulsoFinalizado = false;
  
  // Sincronización de tiempo inicial
  unsigned long tiempoInicio = micros();
  
  // 1. ACTIVAR EXCITACIÓN (Escalón positivo)
  digitalWrite(EXCITACION_PIN, HIGH);
  
  // 2. BUCLE DE CAPTURA DE ALTA VELOCIDAD
  // Captura durante el tiempo definido o hasta llenar el buffer
  while ((micros() - tiempoInicio < CAPTURA_TOTAL) && (muestrasTomadas < MAX_MUESTRAS)) {
    
    // Si ya pasaron los 50ms, bajamos el pulso (Escalón negativo)
    if (!pulsoFinalizado && (micros() - tiempoInicio >= DURACION_PULSO)) {
      digitalWrite(EXCITACION_PIN, LOW);
      pulsoFinalizado = true;
    }

    // Lectura directa del ADC y almacenamiento en RAM
    bufferDatos[muestrasTomadas] = analogRead(SENSOR_PIN);
    muestrasTomadas++;
  }

  // Asegurar que el pin de excitación quede en 0
  digitalWrite(EXCITACION_PIN, LOW);
  
  // 3. ENVÍO DE DATOS A PYTHON
  // Enviamos los datos línea por línea para que Python los procese
  for (int i = 0; i < muestrasTomadas; i++) {
    Serial.println(bufferDatos[i]);
  }
  
  // Marcador de fin de ráfaga
  Serial.println("FIN");
}
