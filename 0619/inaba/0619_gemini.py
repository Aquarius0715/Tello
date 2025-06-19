from djitellopy import Tello
import cv2
import time
import os

def check_tello_battery(tello):
    """
    Telloドローンのバッテリー残量を確認します。
    Args:
        tello (Tello): 初期化されたTelloオブジェクト。
    Returns:
        bool: バッテリー残量が十分であればTrue、そうでなければFalse。
    """
    print("Telloに接続中...")
    tello.connect()
    battery_level = tello.get_battery()
    print(f"バッテリー残量: {battery_level}%")

    if battery_level < 20: # バッテリー残量が20%未満の場合は警告
        print("警告: バッテリー残量が低いです。充電してから撮影してください。")
        return False
    return True

def tello_takeoff(tello):
    """
    Telloドローンを離陸させます。
    Args:
        tello (Tello): 初期化されたTelloオブジェクト。
    """
    print("離陸します...")
    tello.takeoff()
    time.sleep(5)  # 安定するまで待機
    print("離陸しました。")

def capture_360_panorama_at_height(tello, target_height_cm, num_images=12, delay_between_shots=2, output_filename_prefix="panorama", image_dir="C:/Users/takashi/Documents/tello/0619/images"):
    """
    指定された高さでTelloドローンを使用して360度パノラマ画像を撮影し、スティッチングします。

    Args:
        tello (Tello): 初期化されたTelloオブジェクト。
        target_height_cm (int): パノラマを撮影する目標の高さ（cm）。
        num_images (int): 360度を撮影するために必要な画像の枚数。
        delay_between_shots (int): 各画像撮影間の待機時間（秒）。
        output_filename_prefix (str): 生成されるパノラマ画像のファイル名プレフィックス（例: "panorama_2m"）。
        image_dir (str): 撮影した画像を一時的に保存するディレクトリ名。
    """

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    print(f"\n高さ {target_height_cm / 100:.1f}m へ移動します...")
    tello.go_xyz_speed(0, 0, target_height_cm, 50) # x, y, z (cm), speed (cm/s)
    time.sleep(5) # 移動と安定を待機

    # 現在の高さに調整（正確な位置ではないため、微調整は難しい）
    # print(f"現在の高さ: {tello.get_height()}cm")

    tello.streamon()
    frame_read = tello.get_frame_read()

    print(f"高さ {target_height_cm / 100:.1f}m で360度パノラマ撮影を開始します...")

    # 各画像間の回転角度を計算
    degrees_per_shot = 360 / num_images
    captured_images = []

    for i in range(num_images):
        print(f"  画像 {i+1}/{num_images} を撮影中...")

        # 画像をキャプチャ
        frame = frame_read.frame
        if frame is None:
            print("  フレームの取得に失敗しました。スキップします。")
            continue

        # ファイル名に高さと画像番号を含める
        img_path = os.path.join(image_dir, f"{output_filename_prefix}_H{target_height_cm}_{i:02d}.jpg")
        cv2.imwrite(img_path, frame)
        captured_images.append(img_path)
        print(f"  画像を保存しました: {img_path}")

        # 次の画像のための回転
        if i < num_images - 1:
            # Telloは正確な角度で停止するのが難しい場合があるので、少し多めに回すことも検討
            tello.rotate_clockwise(int(degrees_per_shot))
            time.sleep(delay_between_shots) # ドローンが安定するまで待機

    print(f"高さ {target_height_cm / 100:.1f}m での全ての画像の撮影が完了しました。")
    tello.streamoff()

    # 画像のスティッチング
    print(f"  高さ {target_height_cm / 100:.1f}m での画像のスティッチングを開始します...")
    stitcher = cv2.Stitcher_create()

    images_to_stitch = []
    for img_path in captured_images:
        img = cv2.imread(img_path)
        if img is not None:
            images_to_stitch.append(img)
        else:
            print(f"  画像の読み込みに失敗しました: {img_path}")

    if not images_to_stitch:
        print("  スティッチングできる画像がありません。スキップします。")
        return

    # スティッチング処理の実行
    status, panorama = stitcher.stitch(images_to_stitch)

    output_path = f"{output_filename_prefix}_H{target_height_cm}_panorama.jpg"
    if status == cv2.Stitcher.OK:
        cv2.imwrite(output_path, panorama)
        print(f"  高さ {target_height_cm / 100:.1f}m のパノラマ画像を保存しました: {output_path}")
        cv2.imshow(f"360 Panorama at {target_height_cm / 100:.1f}m", panorama)
        cv2.waitKey(1) # 少し待機して次のウィンドウが開くのを防ぐ
    else:
        print(f"  高さ {target_height_cm / 100:.1f}m でのパノラマ画像のスティッチングに失敗しました。ステータスコード: {status}")
        if status == cv2.Stitcher.ERR_NEED_MORE_IMGS:
            print("  より多くの画像が必要です。")
        elif status == cv2.Stitcher.ERR_HOMOGRAPHY_EST_FAIL:
            print("  ホモグラフィーの推定に失敗しました。画像間の特徴点が不足している可能性があります。")
        elif status == cv2.Stitcher.ERR_CAMERA_PARAMS_ADJUST_FAIL:
            print("  カメラパラメータの調整に失敗しました。")

    # 一時画像の削除（必要であればコメントアウトを外す）
    # for img_path in captured_images:
    #     os.remove(img_path)
    # os.rmdir(image_dir) # ディレクトリ内の画像が全て削除されたらディレクトリも削除

if __name__ == "__main__":
    tello = Tello()

    # パノラマ撮影を行う高さのリスト（cm単位）
    target_heights_cm = [200, 300, 400, 500]

    try:
        # 1. バッテリー残量の確認
        if not check_tello_battery(tello):
            print("バッテリー残量が不足しているため、処理を中断します。")
            exit() # プログラムを終了

        # 2. 離陸
        tello_takeoff(tello)

        # 3. 各高さでのパノラマ撮影
        for i, height in enumerate(target_heights_cm):
            # ファイル名を指定
            panorama_file_name = f"multi_height_panorama_{i+1}"
            capture_360_panorama_at_height(tello, height, output_filename_prefix=panorama_file_name)
            time.sleep(3) # 各高度での撮影後に少し待機

        print("\n全てのパノラマ撮影が完了しました。着陸します。")
        tello.land()
        print("着陸しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        # プログラムが予期せず終了した場合でもTelloを安全に着陸させるための処理
        if tello.is_flying:
            print("エラーのためTelloを着陸させます...")
            tello.land()
        if tello.is_connected:
            tello.end()
        cv2.destroyAllWindows() # 開いているすべてのOpenCVウィンドウを閉じる
