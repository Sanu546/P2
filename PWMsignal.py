import RPi.GPIO as GPIO
import time

# Vælg GPIO pin
ledpin = 12

value = 50 # PWM værdi (0-100)

# Opsætning
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledpin, GPIO.OUT)


def ToolValue(value):
    # Opret PWM objekt
    pi_pwm = GPIO.PWM(ledpin, 20)
    pi_pwm.start(value)
    time.sleep(10)
    pi_pwm.stop()
