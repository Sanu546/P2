
import lgpio
import time

# Vælg GPIO pin
servo = 12 # GPIO pin til servo, det svarer til pin 32 på Rapsberry Pi
FREQ = 50 # Frekvens i Hz


h = lgpio.gpiochip_open(0) # Åbn GPIO chip
lgpio.gpio_claim_output(h, servo) # Sæt GPIO pin som output


def setPwm(dutyCycle):
    lgpio.tx_pwm(h, servo, FREQ, dutyCycle)
    time.sleep(1)

def gripperMove():
    gripperNeutral = 5 # Neutral position for griberen
    setPwm(gripperNeutral) # Sætter dutycycle til 5.5 for at sikre at griberen er i neutral position
    time.sleep(1)
    print("Griber i neutral position")

    print("Indtast dutycycle for åbning af griber (2-10)")
    gripperValue = 0 # Initialiserer gripperValue
    gripperValue = input("Indtast dutycycle for åbning af griber: ")
    gripperValue = int(gripperValue) # Konverterer input til integer
    
    # Tjekker om input er gyldigt
    if gripperValue > 10 or gripperValue < -10:
        print("Ugyldigt input, prøv igen")
        return gripperMove() # Kalder funktionen igen hvis input er ugyldigt
    elif -1 <= gripperValue <= 1:
        print("Ugyldig input, prøv igen")
        return gripperMove()
    elif gripperValue == 5:
        print("Griber i neutral position")
        return gripperMove() # Kalder funktionen igen hvis input er 5

    if gripperValue > 0:
        # Åbner gripperen
        for i in range(5,2,-1):
            setPwm(i)
            time.sleep(0.5)
            if i == gripperValue:
                print("Griber åben")
                break
    elif gripperValue < 0:
        # Lukker gripperen
        for i in range(5,10,1): 
            setPwm(i)
            time.sleep(0.5)
            if i == gripperValue*-1:
                print("Griber lukket")
                break

# dutycycle kan være mellem 0 og 1 
while True:
    gripperMove()






