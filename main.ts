/**
 * =====================================================
 */
/**
 * Ring:bit Scratch Firmware
 */
/**
 * Protocolo UART texto, comandos terminados en '\n'
 */
/**
 * Comandos aceptados (Scratch → micro:bit):
 */
/**
 * F            avanzar
 */
/**
 * B            retroceder
 */
/**
 * L            girar izquierda
 */
/**
 * R            girar derecha
 */
/**
 * S            detener
 */
/**
 * V,<pin>,<a>  servo arbitrario (pin 0/1/2, ángulo 0..180)
 */
/**
 * W,<l>,<r>    ruedas con ángulos crudos 0..180
 */
/**
 * T,<texto>    mostrar texto en la matriz
 */
/**
 * C            limpiar matriz
 */
/**
 * =====================================================
 */
// --- Setup BLE ---
bluetooth.onBluetoothConnected(function () {
    connected = true
    showConnected()
})
bluetooth.onBluetoothDisconnected(function () {
    connected = false
    // Parar el coche por seguridad al perder conexión
    pins.servoWritePin(AnalogPin.P1, 90)
    pins.servoWritePin(AnalogPin.P2, 90)
    showWaiting()
})
// --- Parada de emergencia con botones ---
input.onButtonPressed(Button.A, function () {
    pins.servoWritePin(AnalogPin.P1, 90)
    pins.servoWritePin(AnalogPin.P2, 90)
})
// --- Manejo de comandos ---
function handleCommand (raw: string) {
    if (raw.length == 0) {
        return
    }
    cmd = raw.charAt(0)
    if (cmd == "F") {
        // Avanzar: rueda izq hacia adelante, rueda der hacia adelante
        // Los servos del Ring:bit son continuos: 0 y 180 son extremos opuestos
        pins.servoWritePin(AnalogPin.P1, 0)
        pins.servoWritePin(AnalogPin.P2, 180)
    } else if (cmd == "B") {
        pins.servoWritePin(AnalogPin.P1, 180)
        pins.servoWritePin(AnalogPin.P2, 0)
    } else if (cmd == "L") {
        // Girar izquierda: izq parada, der adelante
        pins.servoWritePin(AnalogPin.P1, 90)
        pins.servoWritePin(AnalogPin.P2, 180)
    } else if (cmd == "R") {
        pins.servoWritePin(AnalogPin.P1, 0)
        pins.servoWritePin(AnalogPin.P2, 90)
    } else if (cmd == "S") {
        pins.servoWritePin(AnalogPin.P1, 90)
        pins.servoWritePin(AnalogPin.P2, 90)
    } else if (cmd == "W") {
        // W,leftAngle,rightAngle
        parts = raw.split(",")
        if (parts.length >= 3) {
            l = parseInt(parts[1])
            r = parseInt(parts[2])
            l = Math.max(0, Math.min(180, l))
            r = Math.max(0, Math.min(180, r))
            pins.servoWritePin(AnalogPin.P1, l)
            pins.servoWritePin(AnalogPin.P2, r)
        }
    } else if (cmd == "V") {
        // V,pin,angle
        parts2 = raw.split(",")
        if (parts2.length >= 3) {
            pinNum = parseInt(parts2[1])
            angle = parseInt(parts2[2])
            angle = Math.max(0, Math.min(180, angle))
            if (pinNum == 0) {
                pins.servoWritePin(AnalogPin.P0, angle)
            } else if (pinNum == 1) {
                pins.servoWritePin(AnalogPin.P1, angle)
            } else if (pinNum == 2) {
                pins.servoWritePin(AnalogPin.P2, angle)
            }
        }
    } else if (cmd == "T") {
        // T,texto
        idx = raw.indexOf(",")
        if (idx >= 0 && idx < raw.length - 1) {
            basic.showString(raw.substr(idx + 1))
        }
    } else if (cmd == "C") {
        basic.clearScreen()
    }
}
bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    raw = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine))
    handleCommand(raw)
})
input.onButtonPressed(Button.AB, function () {
    // Identificación visual al pulsar A+B
    basic.showString(control.deviceName())
})
function showConnected () {
    basic.showIcon(IconNames.Yes)
    basic.pause(300)
    basic.clearScreen()
}
// --- Indicadores visuales ---
function showWaiting () {
    basic.showLeds(`
        . . # . .
        . # . # .
        # . . . #
        . # . # .
        . . # . .
        `)
}
let raw = ""
let idx = 0
let angle = 0
let pinNum = 0
let parts2: string[] = []
let r = 0
let l = 0
let parts: string[] = []
let cmd = ""
let connected = false
bluetooth.startUartService()
// --- Estado inicial ---
pins.servoWritePin(AnalogPin.P1, 90)
pins.servoWritePin(AnalogPin.P2, 90)
showWaiting()
