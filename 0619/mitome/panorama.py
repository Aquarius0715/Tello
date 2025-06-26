from djitellopy import Tello
import cv2
import os
import time

tello = Tello()
tello.connect()

# バッテリー残量を確認（任意）
battery = tello.get_battery()
print(f"バッテリー残量: {battery}%")

tello.takeoff()
tello.move_up(500) # Nm (N00cm) 上昇
time.sleep(5)

tello.streamon() # ビデオストリーム開始

# 画像保存用のディレクトリを作成（任意）
if not os.path.exists("panorama_images"):
    os.makedirs("panorama_images")

# 360度を12分割 = 30度ずつ回転
rotation_angle = 30
num_images = 12

for i in range(num_images):
    print(f"{i+1}/{num_images} 枚目を撮影中...")
    # ストリームからフレームを取得
    frame = tello.get_frame_read().frame

    if frame is not None:
        # 画像を保存（ファイル名を適宜変更してください）
        cv2.imwrite(f"panorama_image_{i:02d}.jpg", frame)
        print(f"panorama_image_{i:02d}.jpg を保存しました。")
    else:
        print("フレームを取得できませんでした。")

    # 最後の撮影後以外は回転
    if i < num_images - 1:
        tello.rotate_clockwise(rotation_angle)
        time.sleep(2) # 回転後、安定するまで少し待つ

tello.streamoff() # ビデオストリーム停止
tello.land()
print("撮影と着陸が完了しました。")

cv2.destroyAllWindows()