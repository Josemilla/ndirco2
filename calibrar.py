#!/usr/bin/env python3
import time
import sys
import serial

PETICION = [0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]
# Rango1 de 0 a 2000 ppm
RANGO1 = [0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, 0x07, 0xd0, 0x8F]
# Rango2 de 0 a 5000 ppm
RANGO2 = [0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, 0x13, 0x88, 0xCB]
# Rango3 de 0 a 10000 ppm
RANGO3 = [0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, 0x27, 0x10, 0x2F]
# Calibración
CALIBRAR = [0xFF, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78]
# Activar autocalibración
ACT_AUTO_CALIBRACION = [0xFF, 0x01, 0x79, 0xA0, 0x00, 0x00, 0x00, 0x00, 0xE6]
# Desactivar autocalibración
DES_AUTO_CALIBRACION = [0xFF, 0x01, 0x79, 0x00, 0x00, 0x00, 0x00, 0x00, 0x86]

sensor = serial.Serial(
        port = '/dev/serial0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

print("Calibración para módulo MH-Z14A.")
print("Asegúrate que el módulo se encuentra a 400PPM, en un habitación muy ventilada o recibe aire del exterior.")
while "La respuesta no es válida":
    respuesta = str(input("¿Calibrar? (s/n): ")).lower().strip()
    if respuesta[0] == 's':
        sensor.write(bytearray(ACT_AUTO_CALIBRACION))
        sensor.write(bytearray(CALIBRAR))
        print("Módulo calibrado.")
        sys.exit(0)
        
    if respuesta[0] == 'n':
        print("Módulo sin calibrar.")
        sys.exit(1)
    
