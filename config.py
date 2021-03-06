from os import getenv

# GV Robot Pi configuration file

DEBUG = not (getenv('ENV', 'local') == 'production')

# Movement
DISTANCE = 10
BASE_SPEED = 150
TURNING_SPEED = 40
MIN_SPEED = 25
MAX_SPEED = 50

# Pinout configuration
## Motors
MOTOR_LEFT_PIN = 6
MOTOR_RIGHT_PIN = 19
MOTOR_LEFT_DIR_PIN=13
MOTOR_RIGHT_DIR_PIN=26

## Sonic sensors
SONIC_TOP_TRG_PIN = 4
SONIC_TOP_ECH_PIN = 14
SONIC_MDL_TRG_PIN = 17
SONIC_MDL_ECH_PIN = 27
SONIC_BTM_TRG_PIN = 21
SONIC_BTM_ECH_PIN = 20

## Servo motor
SERVO_PIN = 12

## IR sensor
IR_ADDR=0x48
IR_CHNL=2

## Buttons
START_BTN=21

## Leds
ACTION_LED=20

# Blocks
BLOCKS_WHITELIST = [ 1 ]
