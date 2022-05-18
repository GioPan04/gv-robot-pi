import GPIO.PCF8591 as ADC
from time import sleep

ADC.setup(0x48)


while True:
  a = ADC.read(2)
  v = a / 255
  print(f"Value: {a} Volt: {v}")
  sleep(0.5)