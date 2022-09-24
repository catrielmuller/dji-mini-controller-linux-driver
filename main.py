import serial, uinput, argparse, time

# Config
eventMaxValue = 32768
events = (
    uinput.BTN_JOYSTICK,
    uinput.ABS_X + (0, 32767, 0, 0),
    uinput.ABS_Y + (0, 32767, 0, 0),
    uinput.ABS_RX + (0, 32767, 0, 0),
    uinput.ABS_RY + (0, 32767, 0, 0),
    uinput.ABS_THROTTLE + (0, 32767, 0, 0),
)

# Process input (min 364, center 1024, max 1684) -> (min 0, center 16384, max 32768)
def parseInput(input, name):
    output = (int.from_bytes(input, byteorder='little') - 364) * 4096 // 165
    if name in invert:
        output = eventMaxValue - output
    return output

def readDevice(serial):
    # Reverse ingineered. Seems any one of the known working pings are okay.
    pingData = bytearray.fromhex('550d04330a0e0300400601f44a')
    try:
        serial.write(pingData)
        data = serial.readline()
        # Reverse-engineered. Controller input seems to always be len 38.
        if len(data) == 38:
            # Reverse-engineered. Whole section done from MITM'ing DJI Flight Simulator.
            lh = parseInput(data[16:18], 'lh')
            lv = parseInput(data[13:15], 'lv')
            rh = parseInput(data[7:9], 'rh')
            rv = parseInput(data[10:12], 'rv')
            cam = parseInput(data[19:21], 'cam')
            return {'lh': lh, 'lv': lv, 'rh': rh, 'rv': rv, 'cam': cam}
    except serial.SerialException as e:
        print('\n\nCould not read/write:', e)

def syncJoystick(state):
    device.emit(uinput.ABS_X, state['lh'], syn=False)
    device.emit(uinput.ABS_Y, state['lv'], syn=False)
    device.emit(uinput.ABS_RX, state['rh'], syn=False)
    device.emit(uinput.ABS_RY, state['rv'], syn=False)
    device.emit(uinput.ABS_THROTTLE, state['cam'])
    
# Init
print('Mavic Mini RC <-> UInput')
parser = argparse.ArgumentParser(description='Mavic Mini RC <-> UInput')
parser.add_argument('-d', '--debug', help="Debug Mode", nargs='*', default=False)
parser.add_argument('-p', '--port', help='RC Serial Port (/dev/ttyACM0)', required=True)
parser.add_argument('-i', '--invert', help='Invert lv, lh, rv, rh, or cam axis', nargs='*', default=['lv', 'rv'])

# Settings
args = parser.parse_args()
invert = frozenset(args.invert)

# Open Joystick
device = uinput.Device(events, 'Mavic Mini RC')
time.sleep(1)

# Open Serial Connection
try:
    serial = serial.Serial(port=args.port, baudrate=115200)
    print('Opened serial device:', serial.name)
except serial.SerialException as e:
    print('Could not open serial device:', e)
    exit(1)

try:
    while True:
        state = readDevice(serial)
        if args.debug:
            print(state)
        if state:
            syncJoystick(state)
except KeyboardInterrupt:
    print('Exiting...')
    serial.close()
