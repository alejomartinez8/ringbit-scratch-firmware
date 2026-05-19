"""

=====================================================

"""
"""

Ring:bit Scratch Firmware

"""
"""

Protocolo UART texto, comandos terminados en '\n'

"""
"""

Comandos aceptados (Scratch → micro:bit):

"""
"""

F            avanzar

"""
"""

B            retroceder

"""
"""

L            girar izquierda

"""
"""

R            girar derecha

"""
"""

S            detener

"""
"""

V,<pin>,<a>  servo arbitrario (pin 0/1/2, ángulo 0..180)

"""
"""

W,<l>,<r>    ruedas con ángulos crudos 0..180

"""
"""

T,<texto>    mostrar texto en la matriz

"""
"""

C            limpiar matriz

"""
"""

=====================================================

"""
# --- Setup BLE ---

def on_bluetooth_connected():
    global connected
    connected = True
    showConnected()
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    global connected
    connected = False
    # Parar el coche por seguridad al perder conexión
    pins.servo_write_pin(AnalogPin.P1, 90)
    pins.servo_write_pin(AnalogPin.P2, 90)
    showWaiting()
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

# --- Parada de emergencia con botones ---

def on_button_pressed_a():
    pins.servo_write_pin(AnalogPin.P1, 90)
    pins.servo_write_pin(AnalogPin.P2, 90)
input.on_button_pressed(Button.A, on_button_pressed_a)

# --- Manejo de comandos ---
def handleCommand(raw: str):
    global cmd, parts, l, r, parts2, pinNum, angle, idx
    if len(raw) == 0:
        return
    cmd = raw.char_at(0)
    if cmd == "F":
        # Avanzar: rueda izq hacia adelante, rueda der hacia adelante
        # Los servos del Ring:bit son continuos: 0 y 180 son extremos opuestos
        pins.servo_write_pin(AnalogPin.P1, 0)
        pins.servo_write_pin(AnalogPin.P2, 180)
    elif cmd == "B":
        pins.servo_write_pin(AnalogPin.P1, 180)
        pins.servo_write_pin(AnalogPin.P2, 0)
    elif cmd == "L":
        # Girar izquierda: izq parada, der adelante
        pins.servo_write_pin(AnalogPin.P1, 90)
        pins.servo_write_pin(AnalogPin.P2, 180)
    elif cmd == "R":
        pins.servo_write_pin(AnalogPin.P1, 0)
        pins.servo_write_pin(AnalogPin.P2, 90)
    elif cmd == "S":
        pins.servo_write_pin(AnalogPin.P1, 90)
        pins.servo_write_pin(AnalogPin.P2, 90)
    elif cmd == "W":
        # W,leftAngle,rightAngle
        parts = raw.split(",")
        if len(parts) >= 3:
            l = int(parts[1])
            r = int(parts[2])
            l = max(0, min(180, l))
            r = max(0, min(180, r))
            pins.servo_write_pin(AnalogPin.P1, l)
            pins.servo_write_pin(AnalogPin.P2, r)
    elif cmd == "V":
        # V,pin,angle
        parts2 = raw.split(",")
        if len(parts2) >= 3:
            pinNum = int(parts2[1])
            angle = int(parts2[2])
            angle = max(0, min(180, angle))
            if pinNum == 0:
                pins.servo_write_pin(AnalogPin.P0, angle)
            elif pinNum == 1:
                pins.servo_write_pin(AnalogPin.P1, angle)
            elif pinNum == 2:
                pins.servo_write_pin(AnalogPin.P2, angle)
    elif cmd == "T":
        # T,texto
        idx = raw.index_of(",")
        if idx >= 0 and idx < len(raw) - 1:
            basic.show_string(raw.substr(idx + 1))
    elif cmd == "C":
        basic.clear_screen()

def on_uart_data_received():
    global raw2
    raw2 = bluetooth.uart_read_until(serial.delimiters(Delimiters.NEW_LINE))
    handleCommand(raw2)
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.NEW_LINE),
    on_uart_data_received)

def on_button_pressed_ab():
    # Identificación visual al pulsar A+B
    basic.show_string(control.device_name())
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def showConnected():
    basic.show_icon(IconNames.YES)
    basic.pause(300)
    basic.clear_screen()
# --- Indicadores visuales ---
def showWaiting():
    basic.show_leds("""
        . . # . .
        . # . # .
        # . . . #
        . # . # .
        . . # . .
        """)
raw2 = ""
idx = 0
angle = 0
pinNum = 0
parts2: List[str] = []
r = 0
l = 0
parts: List[str] = []
cmd = ""
connected = False
bluetooth.start_uart_service()
# --- Estado inicial ---
pins.servo_write_pin(AnalogPin.P1, 90)
pins.servo_write_pin(AnalogPin.P2, 90)
showWaiting()