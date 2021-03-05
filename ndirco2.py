#!/usr/bin/env python3
# Otro script para mostrar los datos del sensot MH-Z14A
# 2021 Josema - josemalive@gmail.com

import time
import serial
import fourletterphat

# Comando para leer la concentración de CO2
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

# Configuramos la conexión serie según los datos del fabricante
sensor = serial.Serial(
        port = '/dev/serial0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

# Configuramos el sensor en el rango de medición de 0 - 2000 ppm. Cuanto más bajo es el rango, mejor es la precición.
sensor.write(bytearray(RANGO1))
# Configuramos el brillo de la pantalla
fourletterphat.set_brightness(5)
# Y limpiamos
fourletterphat.clear()

# Entramos el bucle y no salimos nunca
while True:
    # Enviamos el comando para pedir el valor de CO2
    sensor.write(bytearray(PETICION))
    # Recogemos los nueve bits de la respuesta.
    respuesta = sensor.read(9)
    if len(respuesta) == 9:
        # El valor que buscamos se encuentra en el byte 2 (high byte) y 3 (low byte).
        valor_co2 = (respuesta[2] << 8) | respuesta[3]
        # Esto es una ñapa para mostrar el 5 como un S. ¿Por qué? Porque el dibujo del 5 es un tanto extraño y me gusta mas la de la S.
        cadena = str(valor_co2).replace("5", "S")
        # Imprimos el valor en la pantalla y mostramos.
        fourletterphat.print_number_str(cadena)
        fourletterphat.show()
    # Esperamos un segundo que es la velocidad con la que el sensor MH-Z14A funciona.
    time.sleep(1)
