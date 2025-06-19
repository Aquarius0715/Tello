from djitellopy import Tello
import cv2
import time

tello = Tello()
tello.connect()

tello.takeoff()
tello.move_up(50)
time.sleep(5)

tello.streamon()

# Start drawing the "U" shape
# First leg of the U (move forward)
tello.move_forward(100) # Move forward 100 cm
time.sleep(2)

# Bottom of the U (curve or turn and move)
# For a "U" shape, you can do two 90-degree turns with a forward movement in between,
# or try to approximate a curve. Let's do turns for simplicity.
tello.rotate_clockwise(90) # Turn right 90 degrees
time.sleep(2)
tello.move_forward(50) # Move forward for the base of the U
time.sleep(2)
tello.rotate_clockwise(90) # Turn right another 90 degrees
time.sleep(2)

# Second leg of the U (move forward)
tello.move_forward(100) # Complete the U shape by moving forward again
time.sleep(2)


tello.streamoff()

tello.land()
