from djitellopy import Tello
import cv2
import time

tello = Tello()
tello.connect()

tello.takeoff()
tello.move_up(50)
time.sleep(5)

# U
tello.move_forward(50)
time.sleep(5)
tello.rotate_counter_clockwise(90)
time.sleep(5)
tello.move_forward(50)
time.sleep(5)
tello.rotate_counter_clockwise(90)
time.sleep(5)
tello.move_forward(50)
time.sleep(5)

tello.land()