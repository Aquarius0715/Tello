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
        print(f"[TIMEOUT] {command} の応答なし")
    except Exception as e:
        print(f"[ERROR] {command} の送信エラー: {e}")

def draw_h():
    print("[DRAW] H")
    send_command("back 60")
    send_command("forward 30")
    send_command("cw 90")
    send_command("forward 40")  # 中央の横棒
    send_command("ccw 90")
    send_command("forward 30")

def draw_e():
    print("[DRAW] E")
    send_command("back 60")
    send_command("cw 90")
    send_command("forward 40")  # 上横棒
    send_command("back 40")
    send_command("ccw 90")
    send_command("forward 30")
    send_command("cw 90")
    send_command("forward 40")  # 中横棒
    send_command("back 40")
    send_command("ccw 90")
    send_command("forward 30")
    send_command("cw 90")
    send_command("forward 40")  # 下横棒
    send_command("ccw 90")

def draw_l():
    print("[DRAW] L")
    send_command("back 60")
    send_command("cw 90")
    send_command("forward 40")  # 横棒
    send_command("ccw 90")

def move_to_next_letter():
    send_command("right 80")

def main():
    print("Tello: HEL飛行開始")

    send_command("command", wait=2)
    send_command("takeoff", wait=7)
    send_command("up 100", wait=3)

    draw_h()
    move_to_next_letter()
    draw_e()
    move_to_next_letter()
    draw_l()

    send_command("land", wait=5)
    sock.close()
    print("Tello: HEL飛行完了")

if __name__ == "__main__":
    main()
