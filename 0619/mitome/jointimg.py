import cv2
import os

def create_panorama_from_images(image_folder="panorama_images", output_filename="360_panorama_combined.jpg"):
    """
    指定されたフォルダ内の画像ファイル（ファイル名がソート順に並ぶことを前提）を読み込み、
    OpenCVのStitcher機能を使用してパノラマ画像を生成します。

    Args:
        image_folder (str): 画像ファイルが保存されているフォルダのパス。
        output_filename (str): 生成されるパノラマ画像のファイル名。
    """
    img_list = []
    
    # フォルダ内のJPGファイルを読み込み、ファイル名でソート
    # 例: panorama_image_00.jpg, panorama_image_01.jpg ... の順に読み込む
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
    image_files.sort() # ファイル名をソートすることで、撮影順に画像を処理

    if not image_files:
        print(f"エラー: '{image_folder}' フォルダに画像が見つかりませんでした。")
        return

    print(f"'{image_folder}' フォルダから {len(image_files)} 枚の画像を読み込みます。")

    for filename in image_files:
        filepath = os.path.join(image_folder, filename)
        img = cv2.imread(filepath)
        if img is not None:
            img_list.append(img)
        else:
            print(f"警告: '{filepath}' を読み込めませんでした。画像ファイルが破損しているか、パスが間違っている可能性があります。")

    if not img_list:
        print("エラー: 読み込める有効な画像がありませんでした。")
        return

    print(f"{len(img_list)} 枚の画像を結合します...")

    # OpenCVのStitcherオブジェクトを作成
    # デフォルトのモード（PANORAMA）で作成します
    stitcher = cv2.Stitcher.create()

    # 画像のスティッチングを実行
    status, panorama = stitcher.stitch(img_list)

    if status == cv2.Stitcher_OK:
        # パノラマ画像を保存
        cv2.imwrite(output_filename, panorama)
        print(f"✅ パノラマ画像を '{output_filename}' として保存しました！")
        
        # 結果を表示
        print("生成されたパノラマ画像を表示します。キーを押すとウィンドウが閉じます。")
        cv2.imshow("Generated Panorama", panorama)
        cv2.waitKey(0) # キーが押されるまで待機
        cv2.destroyAllWindows() # すべてのOpenCVウィンドウを閉じる
    elif status == cv2.Stitcher_ERR_NEED_MORE_IMGS:
        print("❌ パノラマ結合に失敗しました: より多くの画像が必要です。または、画像間の重なりが不十分で特徴点が十分に検出できませんでした。")
    elif status == cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL:
        print("❌ パノラマ結合に失敗しました: ホモグラフィ推定（画像の位置合わせ）に失敗しました。画像間の重なりが少ない、または画像のブレが大きい可能性があります。")
    elif status == cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL:
        print("❌ パノラマ結合に失敗しました: カメラパラメータの調整に失敗しました。")
    else:
        print(f"❌ パノラマ結合に不明なエラーが発生しました。ステータスコード: {status}")

# --- スクリプト実行部 ---
if __name__ == "__main__":
    # 画像が保存されているフォルダを指定
    # この例では、スクリプトと同じディレクトリにある 'panorama_images' フォルダを想定しています。
    # 実際のフォルダ名に合わせて変更してください。
    input_image_directory = "panorama_images" 
    
    # 出力ファイル名を指定
    output_panorama_file = "2m_height_360_panorama.jpg"

    create_panorama_from_images(input_image_directory, output_panorama_file)