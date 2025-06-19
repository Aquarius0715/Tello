import time
import cv2
import os
from djitellopy import Tello

# --- 設定項目 ---
# 写真を保存するフォルダ名
IMAGE_DIR = "panorama_images"
# 何度回転して撮影するか
NUM_PHOTOS = 12
# 1回の回転角度 (360度 / 撮影枚数)
ROTATION_ANGLE = 360 // NUM_PHOTOS
# -----------------

# 保存用フォルダを作成
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Telloオブジェクトを作成
tello = Tello()

# Telloに接続
tello.connect()
print(f"Tello Battery: {tello.get_battery()}%")

# カメラストリームをオン
tello.streamon()
# get_frame_read() を使うと、背景でフレームを読み込み続けるため、最新のフレームを取得できる
frame_read = tello.get_frame_read()

# 離陸
print("Taking off...")
tello.takeoff()
# 少し待機して機体を安定させる
time.sleep(2)

# 写真撮影ループ
for i in range(NUM_PHOTOS):
    # 現在のフレームを取得
    frame = frame_read.frame

    if frame is not None:
        # 画像をファイルに保存
        filename = os.path.join(IMAGE_DIR, f"pano_{i+1:02d}.png")
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")
    else:
        print("Could not get frame.")

    # 機体を回転させる
    print(f"Rotating {ROTATION_ANGLE} degrees...")
    tello.rotate_clockwise(ROTATION_ANGLE)
    # 回転後の安定のために少し待機
    time.sleep(1)

# 着陸
print("Landing...")
tello.land()

# ストリームをオフにする
tello.streamoff()

print("Panorama shooting finished.")