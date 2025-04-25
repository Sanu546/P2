from lgpio
import time

# Vælg GPIO pin
servo = 32 # GPIO pin til servo
FREQ = 50 # Frekvens i Hz

h = lgpio.gpiochip_open(0) # Åbn GPIO chip



def setPwm(dutyCycle):
    lgpio.tx_pwm(h, servo, FREQ, dutyCycle)
    time.sleep(2)

# dutycycle kan være mellem 0 og 1 
while True:
    setPwm(50)





