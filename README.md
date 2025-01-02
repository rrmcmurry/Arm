# Robotic Arm Project

## Overview

This project is just for fun. I got a [diymore Robotic Arm Kit](https://a.co/d/if8emE7) for Christmas.  This kit along with a set of [diymore MG966R servo motors](https://a.co/d/if8emE7) a [PCA9685 servo motor driver](https://a.co/d/9lWJIKU) and a [raspberry pi 3](https://a.co/d/gZCAYc5) constitute all of the components of this robotic arm. Only other things needed are an [Xbox Controller](https://a.co/d/gVA1zVS), some microUSB cables, and power supplies. 

## Assembly

Assemble the arm kit based on the instructions.

I took a generic microUSB cable (the kind that is just for providing power) and I cut the end off, stripped back the two wires and used those wires to power the PCA9685 (plugged into the green terminals on the PCA9685).  The other microUSB cable is plugged into the raspberry pi directly. I found that these need to be plugged in separately rather than plugging them both into the same power adapter. If I plug both USB cables into the same power adapter, it draws too much power and the raspberry pi restarts. Beyond that you'll need 4 female to female cables to connect from the raspberry pi's pins 1, 3, 5, and 9, which are 3.3v, SDA1, SCL1, and Gnd respectively to the PCA9685's VCC, SDA, SCL, and GND pins (on the side that has pins already soldered on).  Once the arm is assembled plug the servos into the sets of pins labeled 0 through 5 in order from the base (servo0) out to the gripper (servo5).  I took some zip ties and some cardboard and used the cardboard as insulator to zip tie the PCA9685 to the side of the arm. Well... to be fair, I initially used double sided tape to attach the PCA9685... and it took me a while to realize why nothing was working. Some of the pins had gone all the way through the tape and were shorting on the aluminum arm. So cardboard was a second choice after a lot of troubleshooting. 

## Initialization

I downloaded and used the [raspberry pi imager](https://www.raspberrypi.com/software/) to flash the raspberry pi OS onto the raspberry pi's MicroSD card.  Go ahead and configure a user and enable SSH up front. I was running entirely headless (i.e. without a keyboard, monitor, mouse, etc) and I had to restart this process at least once to set up a user so I could use SSH to remote in.  Once the image is installed, plug it into the raspberry pi and turn it on. 

I downloaded and used [putty](https://www.putty.org/) to remote into the raspberry pi over SSH. Host Name is "raspberrypi.local". Port is "22". Connection type is "SSH". Under terminal > features > Check the box next to "Disable application keypad mode".  Then back under Session select Default Settings and hit "Save".  Then hit "Open". 
```
Login as: pi
pi@raspberrypi.local's password: {If you didn't set this up earlier, SSH won't work... go back and reimage the SD card and configure a user}
pi@raspberrypi:~ $ 
```
At this point you should be sitting at this terminal. Run the following commands one at a time:
```
sudo apt update && sudo apt upgrade -y 
```
This one will take a while
```
sudo apt install python3-pip
sudo pip3 install inputs
sudo pip3 install adafruit-circuitpython-servokit
```
Then you need to run this to enable the I2C interface.  Look for Interface Options > I2C.  You can also use this tool to enable a wireless network connection under System Options > Wireless LAN. 
```
sudo raspi-config
```

## Programming

In the terminal type in: 
```
nano arm.py 
```
Then open up the arm.py code in this repository. Highlight it all and hit copy or control-C so that it is in your clipboard. Back in the terminal just right click. You should see the contents of arm.py pasted into your nano session.  Hit Control O to write the contents to the file then hit Control X to exit. 

now type:
```
python arm.py
```
and enjoy... 
Control C will kill the process when you're done playing. 
use nano arm.py to edit the code

## Make it always run at startup

Create a service file:
```
sudo nano /etc/systemd/system/arm.service
```
Add the following to this file:
```
[Unit]
Description=Robot Arm Controller
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/arm.py
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
Hit Control O to write the contents to the file. Hit Control X to exit.

The the following commands:
```
sudo systemctl daemon-reload
sudo systemctl enable arm.service
sudo systemctl start arm.service
```
At this point arm.py should always run on startup 

## Usage



## License

This project is shared under the MIT License. Feel free to use, modify, and distribute it.
