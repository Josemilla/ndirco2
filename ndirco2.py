#!/usr/bin/env python3
# Otro script para mostrar los datos del sensot MH-Z14A
# 2021 Josema - josemalive@gmail.com

import time
import serial
# import fourletterphat
import scrollphathd
from scrollphathd.fonts import font3x5

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

BARRA_CO2 = 1600
BRILLO = 0.2

# Configuramos la conexión serie según los datos del fabricante
sensor = serial.Serial(
        port = '/dev/serial0',
        # port = '/dev/ttyS0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

def imprime_scrollphat(dato, largo_barra):
    global BRILLO

    if dato >= 1000:
        x = 1
    else:
        x = 4

    scrollphathd.clear()
    scrollphathd.write_string(str(dato), x=x, y=0, font=font3x5, brightness = BRILLO)
    scrollphathd.fill(BRILLO, 0, 6, largo_barra, 1)
    scrollphathd.show()


# Configuramos el sensor en el rango de medición de 0 - 2000 ppm. Cuanto más bajo es el rango, mejor es la precición.
sensor.write(bytearray(RANGO1))

# Por experiencia, el primer valor devuelto por el sensor es una medida errónea. Así que leemos y descartamos el valor.
sensor.write(bytearray(PETICION))
respuesta = sensor.read(9)
time.sleep(1)

# Volvemos a hacer un a lectura para mostrar el primer valor en la pantalla
sensor.write(bytearray(PETICION))
respuesta = sensor.read(9)
if len(respuesta) == 9:
        # El valor que buscamos se encuentra en el byte 2 (high byte) y 3 (low byte).
        valor_co2_anterior = (respuesta[2] << 8) | respuesta[3]
        imprime_scrollphat(valor_co2_anterior, 0)

# Entramos el bucle y no salimos nunca
while True:
    # Paramos un segundo en cada iteración del bucle
    time.sleep(1)
    # Enviamos el comando para pedir el valor de CO2
    sensor.write(bytearray(PETICION))
    # Recogemos los nueve bits de la respuesta.
    respuesta = sensor.read(9)
    if len(respuesta) == 9:
        # El valor que buscamos se encuentra en el byte 2 (high byte) y 3 (low byte).
        valor_co2 = (respuesta[2] << 8) | respuesta[3]
        # print(valor_co2)
        # print(range(valor_co2_anterior, valor_co2))
        # Calculamos la longitud de la barra. REPASAR ESTO.
        barra = int(valor_co2 / (BARRA_CO2 / 17))
        # Calculamos la direccion de bucle for
        if valor_co2 > valor_co2_anterior:
            direccion_for = 1
        elif valor_co2 < valor_co2_anterior:
            direccion_for = -1
        else:
            imprime_scrollphat(valor_co2, barra)
            continue
        
        # Este for muestra la animación del conteo cuando cambia el valor
        for digito in range(valor_co2_anterior, valor_co2, direccion_for):
            # print(digito)
            imprime_scrollphat(digito, barra)
            time.sleep(0.3)
        valor_co2_anterior = valor_co2
