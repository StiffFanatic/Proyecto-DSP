Proyecto DSP
=============



-------
Proyecto educativo para adquisición, visualización y análisis digital de señales en un circuito RLC. El sistema integra:
- Firmware para ESP32 que genera un escalón de excitación y envía muestras por serial.
- Módulos de adquisición y procesamiento en Python.
- Interfaz gráfica (GUI) para controlar la adquisición, visualizar señales y estimar parámetros del sistema.

Integrantes
-----------
- Juan Manuel Gonzalez Banguero
- Luis José Pinto Gonzalez
- Andres David Nazarith Gomez

Requisitos
----------
- Python 3.8+ (recomendado)
- PlatformIO (para compilar/flash del ESP32)

Dependencias Python
-------------------
Instala las dependencias listadas en `Requerimientos.txt`:

```bash
pip install -r Requerimientos.txt
```

Instalación recomendada (opcional): crear y activar un entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r Requerimientos.txt
```

Firmware ESP32
--------------
El firmware está en `ESP32/src/firmware.ino`. Ajustes relevantes:
- Baudrate de comunicación serial: `460800` (ver `ESP32/platformio.ini`).
- Pines: `EXCITACION_PIN` = 5, `SENSOR_PIN` = 34 (puedes modificarlos en el archivo de firmware si tu conexión difiere).

Compilar y subir desde la línea de comandos (desde la raíz del proyecto):

```bash
cd ESP32
python -m platformio run
python -m platformio run --target upload
```

O usando PlatformIO instalado globalmente:

```bash
cd ESP32
platformio run
platformio run --target upload
```

Ejecución de la GUI
-------------------
Desde la raíz del proyecto ejecuta:

```bash
python main.py
```

El punto de entrada carga `GUI.app.App` y muestra la interfaz para:
- Conectar al ESP32 por puerto serial
- Tomar datos
- Mostrar análisis y FFT
- Simular respuestas teóricas

Tareas definidas (VS Code)
--------------------------
Si usas VS Code, en esta workspace hay tareas útiles:
- `Build ESP32 Firmware` — ejecuta `python -m platformio run` en `ESP32/`.
- `Upload ESP32 Firmware` — ejecuta `python -m platformio run --target upload` en `ESP32/`.
- `Run DSP GUI` — ejecuta `python main.py` desde la raíz.

Pruebas
-------
Hay un script de pruebas básico: `test_proyecto.py`. Puedes ejecutarlo con:

```bash
python test_proyecto.py
```

Datos y resultados
------------------
- Los datos guardados y resultados se colocan en `results/data/`.

Detalles técnicos rápidos
------------------------
- El firmware recoge hasta `MAX_MUESTRAS` muestras (ver `ESP32/src/firmware.ino`) y las envía línea por línea por serial, terminando con la línea `FIN`.
- El muestreo se hace con resolución de 12 bits y el pulso de excitación está activo 50 ms (captura total 100 ms).
- En Python, `Procesamiento/` contiene los módulos de filtrado (`filtro.py`), FFT (`fft.py`) y cálculo de parámetros (`parametros_dinamicos.py`).

Estructura del proyecto
----------------------
```
Proyecto DSP/
├── main.py                 # Punto de entrada (lanza la GUI)
├── GUI/                    # Interfaz gráfica (app y widgets)
├── Procesamiento/          # Módulos de procesamiento (filtro, fft, etc.)
├── Adquisición_de_datos/   # Comunicación y muestreo
├── ESP32/                  # Proyecto PlatformIO con firmware
├── results/data/           # Datos guardados
├── test_proyecto.py        # Script de pruebas
└── Requerimientos.txt      # Dependencias Python
```

Notas
-----------------
Si encuentras problemas con la comunicación serial, verifica el puerto COM y que la velocidad (`460800`) coincida en ambos extremos. Para preguntas sobre el código, revisa los módulos dentro de `GUI/`, `Procesamiento/` y `Adquisición_de_datos/`.

