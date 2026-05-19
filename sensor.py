import os
import json
import time
from datetime import datetime

# CONFIGURACIÓ: ID del sensor real bus 1-Wire
SENSOR_ID = "28-XXXXXXXXXXXX" # Canviar pel teu ID real
SENSOR_PATH = f"/sys/bus/w1/devices/{SENSOR_ID}/w1_slave"
JSON_FILE = "dades_temperatura.json"

def llegir_temp_real():
    try:
        with open(SENSOR_PATH, "r") as f:
            lines = f.readlines()
            temp_line = lines[1].find("t=")
            if temp_line != -1:
                temp_string = lines[1][temp_line+2:]
                return float(temp_string) / 1000.0
    except Exception as e:
        print(f"Error llegint el sensor: {e}")
        return None

def desar_dades_json():
    temp = llegir_temp_real()
    if temp is not None:
        ara = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nova_lectura = {"data_hora": ara, "temperatura": round(temp, 2)}
        
        # Llegir dades existents si el fitxer existeix
        dades = []
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r") as f:
                try:
                    dades = json.load(f)
                except json.JSONDecodeError:
                    dades = []
        
        # Afegir la nova lectura
        dades.append(nova_lectura)
        
        # Desar el fitxer JSON actualitzat
        with open(JSON_FILE, "w") as f:
            json.dump(dades, f, indent=4)
        print(f"Dada real guardada en JSON: {temp}ºC a les {ara}")

if __name__ == "__main__":
    # Bucle de proves: Execució cada 30 segons com demana l'enunciat
    print("Iniciant monitorització en mode proves (Cada 30 segons)...")
    try:
        while True:
            desar_dades_json()
            time.sleep(30)
    except KeyboardInterrupt:
        print("Monitorització aturada per l'usuari.")
