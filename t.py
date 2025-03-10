import socket

def check_port(host, port):
    # ایجاد یک شیء socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)  # تنظیم زمان انتظار برای اتصال

    # تست اتصال به پورت
    result = sock.connect_ex((host, port))

    # بستن socket
    sock.close()

    # بررسی نتیجه
    if result == 0:
        print(f"Port {port} on {host} is open.")
    else:
        print(f"Port {port} on {host} is closed or unreachable (Error code: {result}).")

# تست پورت 80 روی localhost
check_port("127.0.0.1", 5500)