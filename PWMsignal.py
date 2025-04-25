from gpiozero import PWMLED
import time

# Vælg GPIO pin
pwm = PWMLED(12)



def setPwm(dutyCycle):
    pwm.value = dutyCycle
    time.sleep(2)

# dutycycle kan være mellem 0 og 1 
while True:
    setPwm(0.5)





