import pandas as pd
import os
from datetime import datetime

class DataIO:
    def __init__(self, folder="results/data"):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)

    def guardar_datos(self, t, y):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rlc_data_{timestamp}.csv"
        path = os.path.join(self.folder, filename)

        df = pd.DataFrame({
            "time_s": t,
            "voltage_v": y
        })
        df.to_csv(path, index=False)

        return path

    def cargar_datos(self, path):
        df = pd.read_csv(path)
        return df["time_s"].values, df["voltage_v"].values