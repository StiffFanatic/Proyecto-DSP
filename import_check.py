import sys
import importlib

mods = [
    'main',
    'GUI.app',
    'GUI.ventana',
    'GUI.botones',
    'Procesamiento.data',
    'Procesamiento.filtro',
    'Procesamiento.fdt',
    'Procesamiento.parametros_dinamicos',
    'Adquisición_de_datos.muestreo'
]

for mod in mods:
    try:
        importlib.import_module(mod)
        print('OK', mod)
    except Exception as e:
        print('ERR', mod, type(e).__name__, e)

