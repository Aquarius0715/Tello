from djitellopy import Tello
import cv2
import time

tello = Tello()
tello.connect()

tello.takeoff()
tello.move_up(50)
time.sleep(5)

tello.streamon()

# U
tello.move_forward(100)
time.sleep(3)
tello.rotate_clockwise(90)
time.sleep(3)
tello.move_forward(50)
time.sleep(3)
tello.rotate_clockwise(90)
time.sleep(3)
tello.move_forward(100)
time.sleep(3)

# O
for i in range(8):
    tello.move_forward(30)
    time.sleep(3)
    tello.rotate_clockwise(45)
    time.sleep(3)

# P



tello.streamoff()

tello.land()