
#import lgpio
import time

# Vælg GPIO pin
servo = 12 # GPIO pin til servo, det svarer til pin 32 på Rapsberry Pi
FREQ = 50 # Frekvens i Hz


#h = lgpio.gpiochip_open(0) # Åbn GPIO chip
#lgpio.gpio_claim_output(h, servo) # Sæt GPIO pin som output


def manualPwm():
    # Initialiserer dutyCycle
    dutyCycle = 0 
    # dutyCycle 6 svarer til helt lukket gripper og 3 svarer til helt åben gripper
    dutyCycle = input("Indtast dutycycle (3-6):")
    dutyCycle = float(dutyCycle)
    # Tjekker om input er gyldigt
    if dutyCycle > 6 or dutyCycle < 3:
        print("Ugyldigt input, prøv igen")
        return manualPwm()

    #lgpio.tx_pwm(h, servo, FREQ, dutyCycle)
    time.sleep(.0001)

def pwm(value):
    #lgpio.tx_pwm(h, servo, FREQ, value)
    time.sleep(.0001)



# dutycycle kan være mellem 2 og 10, på gripperen er 3 helt åben og 6 helt lukket 
#while True:
    #manualPwm()