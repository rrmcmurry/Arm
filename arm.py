import select
from adafruit_servokit import ServoKit
from evdev import InputDevice, ecodes

controller = InputDevice('/dev/input/event0')

kit = ServoKit(channels=16)

# Servo assignments
servos = {
    "shoulder": kit.servo[0],
    "bicep": kit.servo[1],
    "elbow": kit.servo[2],
    "flexor": kit.servo[3],
    "wrist": kit.servo[4],
    "grip": kit.servo[5]
}

# Initial angles
angles = {
    "shoulder": 90,
    "bicep": 0,
    "elbow": 0,
    "flexor": 180,
    "wrist": 90,
    "grip": 110,
}

# Track controller states
control_state = {
    "LX": 0,
    "LY": 0,
    "LT": 0,
    "RX": 0,
    "RY": 0,
    "DpadY": 0,
}

buttoncodes = {
    0: "LX",           # ABS_X
    1: "LY",           # ABS_Y
    2: "LT",           # ABS_Z
    3: "RX",           # ABS_RX
    4: "RY",           # ABS_RY
    5: "RT",           # ABS_RZ
    16: "DpadX",       # ABS_HAT0X
    17: "DpadY",       # ABS_HAT0Y
    304: "A",          # BTN_SOUTH
    305: "B",          # BTN_EAST
    307: "X",          # BTN_WEST
    308: "Y",          # BTN_NORTH
    310: "LB",         # BTN_TL
    311: "RB",         # BTN_TR
    314: "Back",       # BTN_SELECT
    315: "Start",      # BTN_START
    316: "Guide",      # BTN_MODE (Xbox logo)
    317: "LStick",     # BTN_THUMBL
    318: "RStick",     # BTN_THUMBR
}

# Deadband and clamp helper functions
def deadband(value, threshold):
    return 0 if abs(value) < threshold else value

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def map_value(value, in_min, in_max, out_min, out_max, deadband=1000):
    return 0 if abs(value) < deadband else int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


# Main loop
while True:

    # Check for events
    r, _, _ = select.select([controller.fd], [], [], 0.01)

    # if there are events, update the control state
    if r:
        events = controller.read()
        for event in events:
            if event.type == ecodes.EV_ABS or event.type == ecodes.EV_KEY:
                button = buttoncodes[event.code]
                if button in control_state:
                    control_state[button] = event.value
                if button == "Start":
                    # Start button -> Exit (restart)
                    exit(0)


    # Update target angles
    angles["shoulder"] += map_value(control_state["LX"], -32768, 32767, 2, -2)
    angles["bicep"] += map_value(control_state["LY"], -32768, 32767, 2, -2)
    angles["elbow"] += map_value(control_state["LY"], -32768, 32767, 2, -2)
    angles["grip"] = map_value(control_state["LT"], 0, 255, 110, 180, 0)
    angles["wrist"] += map_value(control_state["RX"], -32768, 32767, 5, -5)
    angles["flexor"] += map_value(control_state["RY"], -32768, 32767, 2, -2)
    angles["elbow"] += control_state["DpadY"]

    # Update servos
    for name, servo in servos.items():
        angles[name] = clamp(angles[name], 0, 180)
        servo.angle = angles[name]
