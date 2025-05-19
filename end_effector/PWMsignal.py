
###### Uncomment the following lines to use lgpio library, when running on Raspberry Pi ######
# import lgpio

# h = lgpio.gpiochip_open(0) # Åbn GPIO chip

# # Sæt GPIO pin som output
# #------------------------------------------------------------------------------
# lgpio.gpio_claim_output(h, 14)#pin 13 på uno
# lgpio.gpio_claim_output(h, 15)#pin 12 på uno
# lgpio.gpio_claim_output(h, 18)#pin 11 på uno 
# lgpio.gpio_claim_output(h, 23)#pin 10 på uno 
# #------------------------------------------------------------------------------
 
# def setServoPos(pos):
#     if pos == "lidopen":
#         lgpio.gpio_write(h, 14, 1)
#         lgpio.gpio_write(h, 15, 0)
#         lgpio.gpio_write(h, 18, 0)
#         lgpio.gpio_write(h, 23, 0)
#     elif pos == "lidclose":
#         lgpio.gpio_write(h, 14, 0)
#         lgpio.gpio_write(h, 15, 1)
#         lgpio.gpio_write(h, 18, 0)
#         lgpio.gpio_write(h, 23, 0)
#     elif pos == "blockopen":
#         lgpio.gpio_write(h, 14, 0)
#         lgpio.gpio_write(h, 15, 0)
#         lgpio.gpio_write(h, 18, 1)
#         lgpio.gpio_write(h, 23, 0)
#     elif pos == "blockclose":
#         lgpio.gpio_write(h, 14, 0)
#         lgpio.gpio_write(h, 15, 0)
#         lgpio.gpio_write(h, 18, 0)
#         lgpio.gpio_write(h, 23, 1)
#     else:
#         print("Invalid input")


##### Comment the following lines to stop redefining setServoPO(), when running on Raspberry Pi #####
def setServoPos(pos):
    pass