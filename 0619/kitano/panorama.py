import socket
import cv2
import time
import os

TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_VIDEO_PORT = 11111
tello_address = (TELLO_IP, TELLO_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)

def send_command(command, wait=2):
    try:
        sock.sendto(command.encode('utf-8'), tello_address)
        print(f"[SEND] {command}")
        response, _ = sock.recvfrom(1024)
        print(f"[RECV] {response.decode('utf-8')}")
        time.sleep(wait)
    except Exception as e:
        print(f"[ERROR] {e}")

def capture_panorama_at_height(cap, height_label, num_photos=12, angle_step=360//12):
    dir_path = f"panorama/{height_label}"
    os.makedirs(dir_path, exist_ok=True)

    print(f"[📷] {height_label}の高さでパノラマ撮影開始")
    for i in range(num_photos):
        ret, frame = cap.read()
        if ret:
            filename = f"{dir_path}/img_{i:02d}.jpg"
            cv2.imwrite(filename, frame)
            print(f"  → 保存: {filename}")
        else:
            print(f"⚠️ 画像取得失敗")
        send_command(f"cw {angle_step}", wait=2)
        time.sleep(1)

def create_panorama_from_dir(height_label):
    dir_path = f"panorama/{height_label}"
    images = []
    for fname in sorted(os.listdir(dir_path)):
        if fname.endswith(".jpg"):
            img = cv2.imread(os.path.join(dir_path, fname))
            if img is not None:
                images.append(img)

    if len(images) < 2:
        print(f"[⚠️] {height_label}m: 合成用画像が足りません")
        return

    stitcher = cv2.Stitcher_create() if hasattr(cv2, 'Stitcher_create') else cv2.createStitcher()
    status, pano = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        output_path = f"panorama_{height_label}.jpg"
        cv2.imwrite(output_path, pano)
        print(f"[✅] パノラマ画像保存: {output_path}")
    else:
        print(f"[❌] パノラマ合成失敗 @ {height_label}")

def main():
    heights = {
        "2m": 200
    }

    send_command("command")
    send_command("streamon")
    cap = cv2.VideoCapture(f'udp://@0.0.0.0:{TELLO_VIDEO_PORT}')
    time.sleep(2)

    send_command("takeoff", wait=5)
    time.sleep(2)

    for label, move_cm in heights.items():
        send_command(f"up {move_cm}", wait=4)
        capture_panorama_at_height(cap, label)

    send_command("land", wait=5)
    send_command("streamoff")
    cap.release()
    sock.close()

    # パノラマ合成
    for label in heights.keys():
        create_panorama_from_dir(label)

if __name__ == "__main__":
    main()
