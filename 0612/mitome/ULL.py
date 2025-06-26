from djitellopy import Tello
import cv2
import time

tello = Tello()
tello.connect()

tello.takeoff()
tello.move_up(50)
time.sleep(2)

tello.streamon()

# U
tello.move_forward(100)
time.sleep(1)
tello.rotate_counter_clockwise(90)
time.sleep(1)
tello.move_forward(50)
time.sleep(1)
tello.rotate_counter_clockwise(90)
time.sleep(1)
tello.move_forward(100)
time.sleep(1)

# U -> L
tello.rotate_clockwise(90)
time.sleep(1)
tello.move_forward(50)
time.sleep(1)
tello.rotate_clockwise(90)
time.sleep(1)

# L
tello.move_forward(100)
time.sleep(1)
tello.rotate_counter_clockwise(90)
time.sleep(1)
tello.move_forward(50)
time.sleep(1)

# L -> L
tello.rotate_counter_clockwise(90)
time.sleep(1)
tello.move_forward(100)
time.sleep(1)
tello.rotate_clockwise(90)
time.sleep(1)
tello.move_forward(50)
time.sleep(1)

# L
tello.rotate_clockwise(90)
time.sleep(1)
tello.move_forward(50)
time.sleep(1)
tello.rotate_counter_clockwise(90)
time.sleep(1)
tello.move_forward(50)

tello.streamoff()

tello.land()