import socket
import time

TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
tello_address = (TELLO_IP, TELLO_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)

def send_command(command, wait=5):
    try:
        sock.sendto(command.encode('utf-8'), tello_address)
        print(f"[SEND] {command}")
        response, _ = sock.recvfrom(1024)
        decoded = response.decode('utf-8')
        print(f"[RECV] {decoded}")
        if decoded == "error":
            print(f"[WARN] コマンド '{command}' に対して error が返されました")
        time.sleep(wait)
    except socket.timeout:
        print(f"[TIMEOUT] コマンド '{command}' の応答なし")
    except Exception as e:
        print(f"[ERROR] コマンド '{command}' の送信エラー: {e}")

def draw_l_shape():
    """
    空中で 'L' の文字を描く動作：
    - 縦に降下（後退）
    - 90度旋回
    - 横に進む
    """
    segment = 80  # Lの縦棒と横棒の長さ（cm）
    wait = 3

    # 下に縦線を描く
    send_command(f"back {segment}", wait)

    # 右へ向きを変えて横線
    send_command("cw 90", wait)
    send_command(f"forward {segment}", wait)

def main():
    print("Tello: L字飛行 開始")

    send_command("command", wait=2)
    send_command("takeoff", wait=7)
    send_command("up 100", wait=3)

    draw_l_shape()

    send_command("land", wait=5)
    sock.close()
    print("Tello: L字飛行 完了")

if __name__ == "__main__":
    main()
