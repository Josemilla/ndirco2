#!/usr/bin/env python3
# Otro script para mostrar los datos del sensot MH-Z14A
# 2021 Josema - josemalive@gmail.com

import time
import serial
import fourletterphat

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

sensor.write(bytearray(RANGO1))
fourletterphat.set_brightness(5)
fourletterphat.clear()

while True:
    sensor.write(bytearray(PETICION))
    response = sensor.read(9)
    if len(response) == 9:
        valor_co2 = (response[2] << 8) | response[3]
        cadena = str(valor_co2).replace("5", "S")
        fourletterphat.print_number_str(cadena)
        fourletterphat.show()
    time.sleep(0.4)
