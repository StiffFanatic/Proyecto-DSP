Proyecto DSP
==============

Objetivo del proyecto:

Desarrollar un sistema con interfaz gráfica para la adquisición, visualización ya 
análisis digital de señales en un circuito RLC, utilizando ESP32 y 
procesamiento en Python para facilitar el aprendizaje de los estudiantes de los 
circuitos de segundo orden.

## Integrantes
- Juan Manuel Gonzalez Banguero
- Luis Jóse Pinto Gonzalez
- Andres David Nazarith Gomez

## Dependencias
- numpy
- scipy
- pandas
- matplotlib
- control
- pyserial
- Pillow

## Instalación

### Dependencias de Python
```bash
pip install -r Requerimientos.txt
```

### PlatformIO (para firmware ESP32)
PlatformIO es necesario para compilar y subir el firmware al ESP32.

Instálalo con:
```bash
pip install platformio
```

O globalmente:
```bash
pip install --user platformio
```

Verifica la instalación:
```bash
platformio --version
```

## Uso

### Ejecutar la aplicación
```bash
python main.py
```

### Probar con datos de ejemplo
```bash
python test_proyecto.py
```

### Compilar firmware ESP32
En el directorio `ESP32/` hay un proyecto PlatformIO que compila el firmware del ESP32.

```bash
cd ESP32
platformio run
```

Para flashear al ESP32:

```bash
platformio run --target upload
```

El archivo principal del firmware está en `ESP32/src/firmware.ino`.

### Notas de configuración
- `ESP32/platformio.ini` usa la placa `esp32dev`.
- Ajusta `MOSFET_PIN` y `ADC_PIN` en `ESP32/src/firmware.ino` según tu conexión.

### VS Code Tasks
Si trabajas en VS Code, puedes usar las tareas definidas en `.vscode/tasks.json`:
- `Build ESP32 Firmware`
- `Upload ESP32 Firmware`
- `Run DSP GUI`

Asegúrate de tener instalado PlatformIO en VS Code o en la terminal para que estas tareas funcionen.

Esto crea un archivo de datos simulados y verifica que todo el pipeline de procesamiento funcione correctamente.

### Uso de la aplicación GUI

1. **Cargar datos de prueba**: Use el botón "Cargar Datos Prueba" para cargar datos simulados y probar la funcionalidad sin hardware.
2. **Captura de datos reales**: 
   - Conecte el ESP32
   - Presione "Conectar" para establecer comunicación serial
   - Presione "Tomar Datos" para capturar la señal
3. **Análisis**: Presione "Mostrar Análisis" para procesar los datos y estimar parámetros del sistema
4. **Simulación**: Presione "Simular" para generar respuestas teóricas con parámetros RLC personalizados

## Funcionalidades

1. **Adquisición de datos**: Captura señales del ESP32 vía puerto serial
2. **Procesamiento**: Filtrado Butterworth y normalización de señales
3. **Análisis**: Identificación de parámetros del sistema (ζ, ωn, Mp, tp) y cálculo de componentes RLC
4. **Visualización**: Gráficas interactivas, funciones de transferencia y **display de parámetros en GUI**
5. **Simulación**: Generación de respuestas teóricas con parámetros RLC

## Interfaz de usuario

La aplicación muestra en tiempo real:

### Panel de parámetros
- **Parámetros dinámicos**: ζ (amortiguamiento), ωn (frecuencia natural), Mp (sobreimpulso), tp (tiempo al pico)
- **Parámetros RLC**: R (resistencia), L (inductancia), C (capacitancia asumida)

### Gráfica interactiva
- Visualización de señales crudas y procesadas
- Función de transferencia teórica y estimada
- Respuestas simuladas del sistema

## Cálculo de parámetros

### Procesamiento de señal:
1. **Filtrado**: Butterworth lowpass (fc=100Hz) para eliminar ruido
2. **Normalización**: Escalado para que el valor final (steady-state) sea 1.0

### Parámetros dinámicos estimados:
- **ζ (zeta)**: Factor de amortiguamiento
- **ωn**: Frecuencia natural (rad/s)
- **Mp**: Máximo sobreimpulso (%)
- **tp**: Tiempo hasta el pico (s)

### Parámetros RLC calculados:
- **R**: Resistencia (Ω)
- **L**: Inductancia (mH)
- **C**: Capacitancia asumida (1μF)

Los parámetros RLC se calculan asumiendo C = 1μF y resolviendo las ecuaciones del circuito RLC serie.

## Estructura del proyecto
```
Proyecto DSP/
├── main.py                 # Punto de entrada
├── GUI/                    # Interfaz gráfica
├── Procesamiento/          # Módulos de procesamiento
├── Adquisición_de_datos/   # Comunicación con ESP32
├── ESP32/                  # Firmware del ESP32 para escalón MOSFET
├── results/data/           # Datos guardados
├── assets/                 # Recursos gráficos
├── Config/                 # Configuraciones
├── test_proyecto.py        # Script de pruebas
└── requirements.txt        # Dependencias
```
