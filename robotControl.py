from RpiMotorLib import rpi_dc_lib as motorlib
import RPi.GPIO as GPIO
import time


class motorControl(object):
    def __init__(self, speed=25):
        self.speed = speed
        self.Lspeed = self.speed
        self.Rspeed = self.speed
        self.motorL = motorlib.L298NMDc(19, 13, 26, 50, True, "motor_left")
        self.motorR = motorlib.L298NMDc(21, 20, 16, 50, True, "motor_right")
    
    def start(self):
        return self

    def forward(self):
       # while not stopped:
        # self.stop()
        # self.state = 1
        self.motorL.forward(self.Lspeed)
        self.motorR.forward(self.Rspeed)

    def turnL(self):
        self.motorL.stop()
        self.motorR.forward(self.Rspeed)
        time.sleep(0.5)
        self.motorR.stop()

    def turnR(self):
        self.motorR.stop()
        self.motorL.forward(self.Lspeed)
        time.sleep(0.5)
        self.motorL.stop()
    
    def turnB(self):
        self.motorR.stop()
        self.motorL.forward(self.Lspeed)
        time.sleep(self.duration)
        self.motorL.stop()

    def stop(self):
        self.motorL.stop()
        self.motorR.stop()

    def move(self, dir):
        if dir == 'F':
            self.forward()
        elif dir == 'B':
            self.turnB()
        elif dir ==  'L':
            self.turnL()
        elif dir == 'R':
            self.turnR()
        elif dir == 'S':
            self.stop()
        else:
            self.stop()

    def motorDeinit(self):
        self.stop()
        self.motorL.cleanup()
        self.motorR.cleanup()


class gpioControl(object):
    def __init__(self, irPin=5, ledPin=6):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(irPin, GPIO.OUT)
        GPIO.setup(ledPin, GPIO.OUT)
        # these pins are low en
        self.state = {
            'ON': GPIO.LOW,
            'OFF': GPIO.HIGH
        }
        GPIO.output(irPin, self.state['OFF'])
        GPIO.output(ledPin, self.state['OFF'])

    def start(self):
        return self



        


