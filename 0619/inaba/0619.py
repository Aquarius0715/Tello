from djitellopy import Tello
import cv2
import time
import os

def take_picture(numbers):
    num_images = 12
    output_filename_prefix = "panorama"
    image_dir = "C:/Users/takashi/Documents/tello/0619/images"
    time.sleep(5)

    print(f"番号 {numbers}m のパノラマ画像を撮影開始")

    degree = 360 / num_images
    captured_images = []

    for i in range(num_images):
        #画像をキャプチャ
        frame = frame_read.frame

        if frame is None:
            print("フレームが取得できませんでした。")
            continue

        img_path = os.path.join(image_dir, f"{output_filename_prefix}_H{numbers}_{i:02d}.jpg")
        cv2.imwrite(img_path, frame)
        captured_images.append(img_path)
        print(f"画像を保存しました: {img_path}")

        if i < num_images - 1:
            print(f"{degree}度回転します")
            tello.rotate_clockwise(degree)
            time.sleep(5)

    print(f"番号 {numbers}m のパノラマ画像撮影完了")

    stitcher = cv2.Stitcher_create()

    images_to_stitch = []
    for img_path in captured_images:
        img = cv2.imread(img_path)
        if img is not None:
            images_to_stitch.append(img)
        else:
            print(f"画像の読み込みに失敗しました: {img_path}")

    if not images_to_stitch:
        print("スティッチングできる画像がありません。")
        return

    # スティッチング処理の実行
    status, panorama = stitcher.stitch(images_to_stitch)

    output_path = f"{output_filename_prefix}_H{numbers}_panorama.jpg"
    if status == cv2.Stitcher.OK:
        cv2.imwrite(output_path, panorama)
        print(f"パノラマ画像を保存しました: {output_path}")
        cv2.imshow(f"360 Panorama at {numbers}m", panorama)
        cv2.waitKey(1)

    else:
        print("スティッチングに失敗しました。")
        if status == cv2.Stitcher.ERR_NEED_MORE_IMGS:
            print("  より多くの画像が必要です。")
        elif status == cv2.Stitcher.ERR_HOMOGRAPHY_EST_FAIL:
            print("  ホモグラフィーの推定に失敗しました。画像間の特徴点が不足している可能性があります。")
        elif status == cv2.Stitcher.ERR_CAMERA_PARAMS_ADJUST_FAIL:
            print("  カメラパラメータの調整に失敗しました。")


tello= Tello()
tello.connect()

tello.takeoff()

tello.streamon()
time.sleep(5)
frame_read = tello.get_frame_read()

#2m上昇
tello.move_up(200)
#2m地点
take_picture(2)

tello.move_up(100)

#3m地点
take_picture(3)

tello.move_up(100)

#4m地点
take_picture(4)

tello.move_up(100)

#5m地点
take_picture(5)

tello.move_down(500)

tello.streamonoff()

tello.land()
