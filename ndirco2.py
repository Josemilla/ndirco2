#!/usr/bin/env python3
# Otro script para mostrar los datos del sensot MH-Z14A
# 2021 Josema - josemalive@gmail.com

# pip install ephem

import time
import serial
import scrollphathd
from scrollphathd.fonts import font3x5
import ephem
from datetime import datetime as dt
from datetime import timedelta
import math

# Comando para leer la concentración de CO2
PETICION = [0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]
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

MAXIMO_BARRA = 1000
MINIMO_BARRA = 400
BRILLO = None

# Configuramos la conexión serie según los datos del fabricante
sensor = serial.Serial(
        port = '/dev/serial0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1)

scrollphathd.rotate(180)

def imprime_scrollphat(dato):
    global BRILLO
    global MAXIMO_BARRA
    global MINIMO_BARRA

    if dato >= 1000:
        x = 1
    else:
        x = 5

    scrollphathd.clear()
    scrollphathd.write_string(str(dato), x = x, y = 1, font = font3x5, brightness = BRILLO)
    # scrollphathd.fill(BRILLO - 0.1 if BRILLO > 0.1 else BRILLO, 0, 6, int((dato - 400) / ((MAXIMO_BARRA - MINIMO_BARRA) / 17)), 1)
    # scrollphathd.fill(BRILLO - 0.1 if BRILLO > 0.1 else BRILLO, 0, 5, 1, 2)
    # scrollphathd.fill(BRILLO - 0.1 if BRILLO > 0.1 else BRILLO, 8, 5, 1, 2)
    # scrollphathd.fill(BRILLO - 0.1 if BRILLO > 0.1 else BRILLO, 16, 5, 1, 2)
    scrollphathd.show()

def obten_co2():
    # Enviamos el comando para pedir el valor de CO2
    sensor.write(bytearray(PETICION))
    respuesta = sensor.read(9)
    if len(respuesta) == 9:
        # El valor que buscamos se encuentra en el byte 2 (high byte) y 3 (low byte).
        return (respuesta[2] << 8) | respuesta[3]

def ajustar_brillo():
    global BRILLO

    sol = ephem.Sun()
    observador = ephem.Observer()
    # ↓ Define your coordinates here ↓
    observador.lat, observador.lon, observador.elevation = '40.285408', '-3.788855', 660
    # ↓ Set the time (UTC) here ↓
    observador.date = dt.utcnow()
    sol.compute(observador)
    # altitud_sol = sol.alt
    # print(altitud_sol*180/math.pi)
    # -16.8798870431°
    angulo = (sol.alt * 180 / math.pi)
    if  angulo > 0: # Es de día
        BRILLO = 0.3
    else: # Es de noche
        BRILLO = 0.1
    # print (angulo)

# Configuramos el sensor en el rango de medición de 0 - 2000 ppm. Cuanto más bajo es el rango, mejor es la precición.
sensor.write(bytearray(RANGO2))

# Por experiencia, el primer valor devuelto por el sensor es una medida errónea. Así que leemos y descartamos el valor.
obten_co2()
time.sleep(1)

# Volvemos a hacer un a lectura para mostrar el primer valor en la pantalla
valor_co2_anterior = obten_co2()

hora_comprobacion_luz = dt.now()
ajustar_brillo()

imprime_scrollphat(valor_co2_anterior)

# Entramos el bucle y no salimos nunca
while True:
    # Paramos un segundo en cada iteración del bucle
    time.sleep(1)
    valor_co2 = obten_co2()
    # Calculamos la direccion de bucle for
    if valor_co2 > valor_co2_anterior:
        direccion_for = 1
    elif valor_co2 < valor_co2_anterior:
        direccion_for = -1
    else:
        imprime_scrollphat(valor_co2)
        continue
    
    # Este for muestra la animación del conteo cuando cambia el valor
    for digito in range(valor_co2_anterior, valor_co2, direccion_for):
        imprime_scrollphat(digito)
        if abs(valor_co2_anterior - valor_co2) <= 10:
            time.sleep(0.3)
    valor_co2_anterior = valor_co2

    if dt.now() >= (hora_comprobacion_luz + timedelta(minutes=1)):
        # print("Sólo entro aqui cada minuto")
        ajustar_brillo()
        hora_comprobacion_luz = dt.now()