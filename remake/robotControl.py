from RpiMotorLib import rpi_dc_lib as motorlib
import RPi.GPIO as GPIO
import time
from threading import Thread


class motorControl(object):
    def __init__(self, speed=25):
        self.speed = speed
        self.Loffset = 1.0
        self.Roffset = 1.0
        self.Lspeed = self.speed * self.Loffset
        self.Rspeed = self.speed * self.Roffset
        self.duration = 0.5
        self.motorL = motorlib.L298NMDc(19, 13, 26, 50, True, "motor_left")
        self.motorR = motorlib.L298NMDc(20, 21, 16, 50, True, "motor_right")
        self.started = False
        self.dir = 'S'
        self.lastDir = self.dir
        self.thread = Thread(target=self.moveThread, args=())
        self.thread.daemon = True

    def start(self):
        self.started = True

        self.thread.start()


    # def speedUP(self):

    # def s


    def forward(self):
       # while not stopped:
        # self.stop()
        # self.state = 1
        for i in range(0, 100, 10):
            speed = self.speed*i/100
            self.motorL.forward(speed)
            self.motorR.forward(speed)
            time.sleep(0.1)
        time.sleep(1)
        for i in range(0, 100, 10):
            speed = self.speed*(1-i/100)
            self.motorL.forward(speed)
            self.motorR.forward(speed)
            time.sleep(0.1)
#         time.sleep(0.1)
        self.motorL.stop()
        self.motorR.stop()
        self.dir = 'S'

    def turnL(self):
        self.motorL.stop()
        self.motorR.stop()
        self.motorL.backward(self.Lspeed)
        self.motorR.forward(self.Rspeed)
        time.sleep(self.duration)
        self.motorL.stop()
        self.motorR.stop()
        self.dir = 'S'
        # time.sleep(self.duration*0.9)
        # self.motorR.stop()

    def turnR(self):
        self.motorL.stop()
        self.motorR.stop()
        self.motorR.backward(self.Rspeed)
        self.motorL.forward(self.Lspeed)
        time.sleep(self.duration)
        self.motorL.stop()
        self.motorR.stop()
        self.dir = 'S'
        # time.sleep(self.duration*0.9)
        # self.motorL.stop()

    def turnB(self):
        self.motorL.stop()
        self.motorR.stop()
        self.motorR.backward(self.Rspeed)
        self.motorL.forward(self.Lspeed)
        time.sleep(self.duration*1.9)
        self.motorL.stop()
        self.motorR.stop()
        self.dir = 'S'
        # time.sleep(self.duration*0.9)
        # self.motorL.stop()
        # self.motorR.stop()
    
    def isTurning(self):
        if self.dir == 'S':
            return True
        else:
            return False


    def stop(self):
        self.motorL.stop()
        self.motorR.stop()

    def moveThread(self):
        while self.started:
            print("last dir: ", self.lastDir)
            print("dir: ", self.dir)
            
            if self.lastDir != self.dir:
                if self.dir == 'F':
                    self.forward()
                elif self.dir == 'B':
                    self.turnB()
                elif self.dir == 'L':
                    self.turnL()
                elif self.dir == 'R':
                    self.turnR()
                elif self.dir == 'S':
                    self.stop()
                self.lastDir = self.dir
            #self.dir = 'S'
            time.sleep(0.1)

    def move(self, dir):
        self.dir = dir

    def adjust(self, speed, Loffset, Roffset, duration):
        self.speed = speed
        self.Roffset = Roffset
        self.Loffset = Loffset
        self.duration = duration
        self.Lspeed = self.speed * self.Loffset
        self.Rspeed = self.speed * self.Roffset

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
