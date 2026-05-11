#!/usr/bin/env python3
"""
Script de prueba para el Proyecto DSP
Verifica el funcionamiento completo del sistema de análisis de señales RLC
"""

import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Procesamiento.data import DataIO
from Procesamiento.filtro import SignalProcessor
from Procesamiento.parametros_dinamicos import Identificar_sistema
from Procesamiento.fdt import Estimador_FDT

def calcular_parametros_rlc(zeta, wn, C_asumido=1e-6):
    """
    Calcula R, L, C a partir de parámetros dinámicos.
    Asume un valor típico para C y calcula L y R.
    """
    # Para circuito RLC serie:
    # ωn = 1/√(LC)  ⇒  LC = 1/ωn²
    # ζ = R/(2√(L/C))  ⇒  R = 2ζ√(L/C)
    
    # Calcular L a partir de LC = 1/ωn² y C asumido
    LC = 1 / (wn ** 2)
    L = LC / C_asumido
    
    # Calcular R a partir de ζ = R/(2√(L/C))
    sqrt_LC = np.sqrt(L / C_asumido)
    R = 2 * zeta * sqrt_LC
    
    return {
        'R': R,
        'L': L,
        'C': C_asumido
    }

def crear_datos_prueba():
    """Crea un archivo de datos de prueba si no existe"""
    data_folder = "results/data"
    os.makedirs(data_folder, exist_ok=True)

    # Verificar si ya existe un archivo de prueba
    archivos_prueba = [f for f in os.listdir(data_folder) if f.startswith('rlc_data_test_')]
    if archivos_prueba:
        print(f"✅ Ya existe archivo de prueba: {archivos_prueba[0]}")
        return os.path.join(data_folder, archivos_prueba[0])

    print("📝 Creando archivo de datos de prueba...")

    # Parámetros del sistema subamortiguado
    zeta = 0.1   # Amortiguamiento
    wn = 100     # Frecuencia natural (rad/s)
    fs = 1000    # Frecuencia de muestreo (Hz)

    # Tiempo de simulación
    t = np.linspace(0, 2, int(2*fs))

    # Respuesta al escalón subamortiguada
    wd = wn * np.sqrt(1 - zeta**2)  # Frecuencia amortiguada
    phi = np.arctan(zeta / np.sqrt(1 - zeta**2))  # Fase

    # Respuesta teórica
    y_theoretical = 1 - np.exp(-zeta*wn*t) * np.cos(wd*t - phi)

    # Añadir ruido para simular datos reales
    np.random.seed(42)
    noise = np.random.normal(0, 0.01, len(t))
    y_noisy = y_theoretical + noise

    # Guardar archivo
    df = pd.DataFrame({
        'time_s': t,
        'voltage_v': y_noisy
    })

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'rlc_data_test_{timestamp}.csv'
    filepath = os.path.join(data_folder, filename)

    df.to_csv(filepath, index=False)

    print(f"✅ Archivo de prueba creado: {filepath}")
    print(f"   - {len(df)} muestras")
    print(f"   - Sistema: ζ={zeta}, ωn={wn} rad/s")

    return filepath

def probar_pipeline_completo():
    """Prueba completa del pipeline de procesamiento"""
    print("\n🔬 PROBANDO PIPELINE COMPLETO")
    print("=" * 40)

    # 1. Crear/cargar datos de prueba
    test_file = crear_datos_prueba()

    # 2. Cargar datos
    print("\n📂 Cargando datos...")
    data_io = DataIO()
    t, y = data_io.cargar_datos(test_file)

    print(f"✅ Datos cargados: {len(t)} muestras")
    print(f"   Primeros 5 tiempos: {t[:5]}")
    print(f"   Primeros 5 voltajes: {y[:5]}")

    # 3. Procesamiento de señal
    print("\n🔧 Procesando señal...")
    processor = SignalProcessor(fs=1000)
    y_filt = processor.pasa_bajas(y, fc=100)
    y_norm = processor.normalizacion(y_filt)

    print("✅ Procesamiento completado (filtro Butterworth + normalización)")

    # 4. Identificación de parámetros
    print("\n🧮 Identificando parámetros del sistema...")
    identifier = Identificar_sistema(t, y_norm)
    params = identifier.verif_segundo_orden()

    print("📊 Parámetros estimados:")
    print(f"  ζ  = {params['zeta']:.4f}")
    print(f"  ωn = {params['wn']:.2f} rad/s")
    print(f"  Mp = {params['Mp']:.4f}")
    print(f"  tp = {params['t_peak']:.4f} s")

    # Calcular parámetros RLC
    rlc_params = calcular_parametros_rlc(params['zeta'], params['wn'])
    print("🔧 Parámetros RLC calculados (C asumido = 1μF):")
    print(f"  R = {rlc_params['R']:.1f} Ω")
    print(f"  L = {rlc_params['L']:.1f} H")
    print(f"  C = {rlc_params['C']*1e6:.1f} μF")

    # 5. Función de transferencia
    print("\n📐 Generando función de transferencia...")
    tf_est = Estimador_FDT(params['zeta'], params['wn'])
    G_est = tf_est.Obtener_funcion_transferencia()

    print("Función de transferencia estimada:")
    print(G_est)

    # 6. Validación
    print("\n✅ VALIDACIÓN:")
    zeta_esperado = 0.1
    wn_esperado = 100

    error_zeta = abs(params['zeta'] - zeta_esperado) / zeta_esperado * 100
    error_wn = abs(params['wn'] - wn_esperado) / wn_esperado * 100

    print(f"  Error ζ  = {error_zeta:.1f}%")
    print(f"  Error ωn = {error_wn:.1f}%")

    if error_zeta < 10 and error_wn < 10:
        print("🎉 ¡PRUEBA EXITOSA! El sistema funciona correctamente.")
        return True
    else:
        print("⚠️  La estimación tiene errores significativos.")
        return False

def main():
    """Función principal"""
    print("🚀 PRUEBA DEL PROYECTO DSP")
    print("=" * 50)
    print("Sistema de análisis de señales RLC subamortiguado")

    try:
        exito = probar_pipeline_completo()
        if exito:
            print("\n💡 El proyecto está listo para usar.")
            print("   - Conecta el ESP32 para capturar datos reales")
            print("   - O usa el archivo de prueba generado")
        else:
            print("\n❌ Revisar implementación del sistema de identificación")

    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()