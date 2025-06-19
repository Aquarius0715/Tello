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
    try:
        tello.connect()
        battery_level = tello.get_battery()
        print(f"バッテリー残量: {battery_level}%")

        if battery_level < 20: # バッテリー残量が20%未満の場合は警告
            print("警告: バッテリー残量が低いです。充電してから撮影してください。")
            return False
        return True
    except Exception as e:
        print(f"Telloへの接続に失敗しました: {e}")
        print("Telloがオンになっていて、Wi-Fiネットワークに接続されていることを確認してください。")
        return False


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

def capture_360_panorama_at_height(tello, target_height_cm, num_images=12, delay_between_shots=2, output_filename_prefix="panorama", image_dir_base="panorama_images"):
    """
    指定された高さでTelloドローンを使用して360度パノラマ画像を撮影し、スティッチングします。

    Args:
        tello (Tello): 初期化されたTelloオブジェクト。
        target_height_cm (int): パノラマを撮影する目標の高さ（cm）。
        num_images (int): 360度を撮影するために必要な画像の枚数。
        delay_between_shots (int): 各画像撮影間の待機時間（秒）。
        output_filename_prefix (str): 生成されるパノラマ画像のファイル名プレフィックス（例: "panorama_2m"）。
        image_dir_base (str): 撮影した画像を一時的に保存するベースディレクトリ名。
    """
    # 現在のスクリプトのディレクトリを取得し、その中に画像ディレクトリを作成
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(script_dir, image_dir_base)

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    print(f"\n高さ {target_height_cm / 100:.1f}m へ移動します...")
    # tello.go_xyz_speedは非推奨になる可能性があります。
    # 代わりに tello.move_up(), tello.move_down() などを組み合わせて使うことを検討してください。
    # 簡単な高さ移動であれば tello.move_up(target_height_cm) などで十分かもしれません。
    # ただし、go_xyz_speed は x, y, z の相対移動なので、現在位置からの移動になります。
    # ターゲットの絶対高さを目指す場合は、tello.get_height() で現在の高さを取得し、差分を計算して移動させる必要があります。
    # この例では、相対的な高さ移動としてそのまま go_xyz_speed を使用します。
    # また、go_xyz_speed のZ軸は 'up' が正方向です。

    # 現在の高さに調整するため、いったん上昇（または下降）指示
    # Telloの高度計はあまり精密ではないため、go_xyz_speed(0, 0, target_height_cm, speed)は現在の高度からtarget_height_cmだけ移動します。
    # もし絶対的な高さに到達させたい場合は、Tello SDKの制約上、ループで高度をチェックしながら細かく調整する必要があります。
    # 今回は 'target_height_cm' を現在の高さからの「上昇量」として扱います。
    # あるいは、最初のtakeoff後に一回だけgo_xyz_speedで目標高度まで移動し、その後は水平移動と回転のみを行う設計も考えられます。
    # 例: tello.move_up(target_height_cm)

    # ここでは、単純に 'target_height_cm' まで到達するように調整します（ただし、これは相対的な移動になります）
    # より確実な方法としては、TelloSDKの `get_height()` を利用して、現在の高さと目標の高さの差分を計算し、
    # `tello.move_up()` または `tello.move_down()` を使うのが良いでしょう。

    current_height = tello.get_height() # cm
    height_to_move = target_height_cm - current_height

    if height_to_move > 0:
        print(f"  現在の高さ {current_height}cm から {height_to_move}cm 上昇します。")
        tello.move_up(height_to_move)
    elif height_to_move < 0:
        print(f"  現在の高さ {current_height}cm から {-height_to_move}cm 下降します。")
        tello.move_down(-height_to_move)
    else:
        print(f"  すでに目標の高さ {target_height_cm}cm です。")

    time.sleep(5) # 移動と安定を待機
    print(f"  現在の高さ (推定): {tello.get_height()}cm") # 移動後の推定高さ

    tello.streamon()
    frame_read = tello.get_frame_read()

    print(f"高さ {target_height_cm / 100:.1f}m で360度パノラマ撮影を開始します...")

    # 各画像間の回転角度を計算
    degrees_per_shot = 360 / num_images
    captured_images = []

    for i in range(num_images):
        print(f"  画像 {i+1}/{num_images} を撮影中...")

        # 画像をキャプチャ
        frame = frame_read.frame
        if frame is None:
            print("  フレームの取得に失敗しました。スキップします。")
            continue

        # ファイル名に高さと画像番号を含める
        img_path = os.path.join(image_dir, f"{output_filename_prefix}_H{target_height_cm}_{i:02d}.jpg")
        cv2.imwrite(img_path, frame)
        captured_images.append(img_path)
        print(f"  画像を保存しました: {img_path}")

        # 次の画像のための回転
        if i < num_images - 1:
            tello.rotate_clockwise(int(degrees_per_shot))
            time.sleep(delay_between_shots) # ドローンが安定するまで待機

    print(f"高さ {target_height_cm / 100:.1f}m での全ての画像の撮影が完了しました。")
    tello.streamoff()

    # 画像のスティッチング
    print(f"  高さ {target_height_cm / 100:.1f}m での画像のスティッチングを開始します...")
    # OpenCV 4.x以降では、Stitcher_create() が推奨されます。
    # cv2.Stitcher_create(cv2.Stitcher_PANORAMA) はより特定のモードを指定できますが、
    # シンプルに cv2.Stitcher_create() でもパノラマスティッチングが可能です。
    stitcher = cv2.Stitcher_create()

    images_to_stitch = []
    for img_path in captured_images:
        img = cv2.imread(img_path)
        if img is not None:
            images_to_stitch.append(img)
        else:
            print(f"  画像の読み込みに失敗しました: {img_path}")

    if not images_to_stitch:
        print("  スティッチングできる画像がありません。スキップします。")
        return

    # スティッチング処理の実行
    status, panorama = stitcher.stitch(images_to_stitch)

    output_path = os.path.join(script_dir, f"{output_filename_prefix}_H{target_height_cm}_panorama.jpg")
    if status == cv2.Stitcher.OK:
        cv2.imwrite(output_path, panorama)
        print(f"  高さ {target_height_cm / 100:.1f}m のパノラマ画像を保存しました: {output_path}")
        cv2.imshow(f"360 Panorama at {target_height_cm / 100:.1f}m", panorama)
        cv2.waitKey(1) # 少し待機して次のウィンドウが開くのを防ぐ
    else:
        print(f"  高さ {target_height_cm / 100:.1f}m でのパノラマ画像のスティッチングに失敗しました。ステータスコード: {status}")
        if status == cv2.Stitcher.ERR_NEED_MORE_IMGS:
            print("  より多くの画像が必要です。")
        elif status == cv2.Stitcher.ERR_HOMOGRAPHY_EST_FAIL:
            print("  ホモグラフィーの推定に失敗しました。画像間の特徴点が不足している可能性があります。")
        elif status == cv2.Stitcher.ERR_CAMERA_PARAMS_ADJUST_FAIL:
            print("  カメラパラメータの調整に失敗しました。")

    # 一時画像の削除（必要であればコメントアウトを外す）
    # for img_path in captured_images:
    #     os.remove(img_path)
    # os.rmdir(image_dir) # ディレクトリ内の画像が全て削除されたらディレクトリも削除

if __name__ == "__main__":
    tello = Tello()

    # パノラマ撮影を行う高さのリスト（cm単位）
    # `tello.move_up` などは現在の高さからの相対移動です。
    # したがって、`target_heights_cm` は離陸後の「追加の高さ」として扱われるべきか、
    # または最初の `target_heights_cm[0]` で絶対的な目標高さに到達させ、
    # その後は差分で移動させるロジックが必要です。
    # ここでは、各 `height` が `tello.get_height()` で取得できる目標の絶対高さとして扱います。
    # 最初に `tello.takeoff()` で離陸した高さを考慮に入れる必要があります。
    # Telloは離陸後約100cm程度の高さに浮上します。
    # したがって、`target_heights_cm` は `takeoff` 後の地上からの絶対高さとして定義します。
    # 例: 200cm (地上から2m), 300cm (地上から3m)
    target_heights_cm = [200, 300, 400, 500]

    try:
        # 1. バッテリー残量の確認
        if not check_tello_battery(tello):
            print("バッテリー残量が不足しているか、Telloへの接続に失敗したため、処理を中断します。")
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
