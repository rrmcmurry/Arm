from adafruit_servokit import ServoKit
from inputs import devices

kit = ServoKit(channels=16)
controller = devices.gamepads[0]

# Servo assignments
servos = {
    "shoulder": kit.servo[0],
    "bicep": kit.servo[1],
    "elbow": kit.servo[2],
    "flexor": kit.servo[3],
    "wrist": kit.servo[4],
    "grip": kit.servo[5],
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

ABS_HAT0Y = 0

# Deadband and clamp helper functions
def deadband(value, threshold):
    return 0 if abs(value) < threshold else value

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def map_value(value, in_min, in_max, out_min, out_max, deadband=1000):
    return 0 if abs(value) < deadband else int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Update servo function
def update_servo(name, value):
    angles[name] = clamp(value, 0, 180)
    servos[name].angle = angles[name]

# Main loop
while True:
    events = controller.read()
    for event in events:
        if event.code == "ABS_X":
            # Left stick horizontal -> Shoulder
            update_servo("shoulder", angles["shoulder"] + map_value(event.state, -32768, 32767, 2, -2))

        elif event.code == "ABS_Y":
            # Left stick vertical -> ShoulderUp and Elbow
            update_servo("bicep", angles["bicep"] + map_value(event.state, -32768, 32767, 2, -2))
            update_servo("elbow", angles["elbow"] + map_value(event.state, -32768, 32767, 2, -2))

        elif event.code == "ABS_Z":
            # Left trigger -> Grip
            update_servo("grip", map_value(event.state, 0, 255, 110, 180, 0))

        elif event.code == "ABS_RX":
            # Right stick horizontal -> Wrist
            update_servo("wrist", angles["wrist"] + map_value(event.state, -32768, 32767, 5, -5))

        elif event.code == "ABS_RY":
            # Right stick vertical -> Wrist flexor
            update_servo("flexor", angles["flexor"] + map_value(event.state, -32768, 32767, 2, -2))

        elif event.code == "ABS_HAT0Y":
            ABS_HAT0Y = event.state

        if ABS_HAT0Y != 0:
            update_servo("elbow", angles["elbow"]+ABS_HAT0Y)
