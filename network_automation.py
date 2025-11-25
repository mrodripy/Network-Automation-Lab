import os
from netmiko import ConnectHandler
from datetime import datetime

# Directorio de salida para los archivos.
OUTPUT_DIR = "network_backups"

# --- CONFIGURACIÓN DE DISPOSITIVOS ---
# IMPORTANTE: Reemplaza estos valores con las IPs, usuarios y contraseñas 
# reales de tus dispositivos R1 y SW1 en el laboratorio virtual.

DEVICES = [
    {
        'device_type': 'cisco_ios',
        'host':   '192.168.100.16', # <--- REEMPLAZAR con la IP de R1
        'username': 'admin',
        'password': 'cisco_password', # <--- REEMPLAZAR
        'secret': 'enable_secret' 
    },
    {
        'device_type': 'cisco_ios',
        'host':   '192.168.100.16', # <--- REEMPLAZAR con la IP de SW1
        'username': 'admin',
        'password': 'cisco_password', # <--- REEMPLAZAR
        'secret': 'enable_secret'
    }
]

def run_automation(device_list):
    """Itera sobre la lista de dispositivos para hacer backup y verificación."""
    
    # 1. Crear el directorio de salida si no existe
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Directorio '{OUTPUT_DIR}' creado.")

    commands_to_verify = [
        'show version',
        'show ip interface brief',
        'show cdp neighbor'
    ]
    
    for device in device_list:
        host = device['host']
        print(f"\n--- Iniciando conexión a {host} ---")
        
        try:
            # Conexión SSH usando Netmiko
            net_connect = ConnectHandler(**device)
            net_connect.enable()
            
            # Obtener el hostname para nombrar los archivos
            hostname = net_connect.send_command('show version | include uptime').split()[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # --- Tarea 1: Backup de Configuración (show running-config) ---
            print(f"-> Realizando backup de configuración en {hostname}...")
            running_config = net_connect.send_command('show running-config')
            
            backup_filename = os.path.join(OUTPUT_DIR, f"{hostname}_backup_{timestamp}.txt")
            with open(backup_filename, 'w') as f:
                f.write(running_config)
            print(f"✅ Backup guardado en {backup_filename}")
            
            # --- Tarea 2: Ejecutar Comandos de Verificación ---
            print(f"-> Ejecutando comandos de verificación...")
            log_output = net_connect.send_config_set(commands_to_verify)
            
            log_filename = os.path.join(OUTPUT_DIR, f"{hostname}_verification_log_{timestamp}.txt")
            with open(log_filename, 'w') as f:
                f.write(log_output)
            print(f"✅ Log de verificación guardado en {log_filename}")
            
            net_connect.disconnect()
            
        except Exception as e:
            print(f"❌ ERROR en {host}: No se pudo conectar o ejecutar comandos.")
            print(f"Detalle del error: {e}")

if __name__ == "__main__":
    run_automation(DEVICES)