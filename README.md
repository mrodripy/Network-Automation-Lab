# Network-Automation-Lab - Backup Script (Netmiko)

Este es mi primer proyecto de automatización de red, creado como parte de mi plan de 6 meses para dominar NetDevOps.

## Descripción
El script `network_automation.py` se conecta vía SSH a múltiples dispositivos Cisco (R1, SW1) usando la librería **Netmiko** de Python. 

**Funcionalidad:**
1.  Realiza el backup de la configuración en ejecución (`show running-config`).
2.  Ejecuta comandos de verificación (`show version`, `show ip int brief`).
3.  Guarda los resultados en archivos de texto, organizados por dispositivo y timestamp.

## Pre-requisitos
* Python 3
* Librería `netmiko` (`pip install netmiko`)
* Laboratorio virtual con dispositivos de red accesibles vía SSH.
