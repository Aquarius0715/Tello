from djitellopy import Tello
import time

# --- パラメータ設定 ---
# 1つのカーブで進む前後の距離 (cm)
forward_distance = 50
# 1つのカーブで進む左右の距離 (cm)
side_distance = 50
# 飛行速度 (cm/s)
speed = 40

# --- Telloの準備 ---
tello = Tello()

try:
    # Telloに接続
    tello.connect()
    print(f"バッテリー残量: {tello.get_battery()}%")
    print("S字飛行を開始します。3秒後に離陸します。")
    time.sleep(3)

    # 離陸
    tello.takeoff()
    tello.move_up(100)
    time.sleep(1)

    # --- S字飛行の実行 ---
    print("ステップ1: 右カーブ")
    # 最初のカーブ（右へ）
    # 中間点: (x=50, y=-50, z=0)
    # 最終点: (x=100, y=0, z=0) のようなイメージ
    tello.curve_xyz_speed(forward_distance, -side_distance, 0, forward_distance * 2, 0, 0, speed)
    time.sleep(1)

    print("ステップ2: 左カーブ")
    # 次のカーブ（左へ）
    # 現在地から見て、今度は左にカーブして元の軸に戻る
    tello.curve_xyz_speed(forward_distance, side_distance, 0, forward_distance * 2, 0, 0, speed)
    time.sleep(1)


    # --- 終了処理 ---
    print("着陸します")
    tello.land()
    print("S字飛行完了！")

except Exception as e:
    print(f"エラーが発生しました: {e}")
    tello.land() # エラー時も安全のため着陸を試みる

finally:
    # 接続を終了
    tello.end()