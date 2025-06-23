from djitellopy import Tello
import cv2
import time

tello = Tello()
tello.connect()

tello.takeoff()
tello.move_up(50)
time.sleep(5)

# Hishigata (菱形) の動き
side_length = 100
tello.move_forward(side_length)
time.sleep(1)
tello.rotate_clockwise(120) 
time.sleep(1)
tello.move_forward(side_length)
time.sleep(1)
tello.rotate_clockwise(60)
time.sleep(1)
tello.move_forward(side_length)
time.sleep(1)
tello.rotate_clockwise(120)
time.sleep(1)
tello.move_forward(side_length)
time.sleep(1)
tello.rotate_clockwise(60)
time.sleep(1)

tello.land()