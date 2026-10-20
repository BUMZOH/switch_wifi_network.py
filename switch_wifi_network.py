import json
import subprocess
import time


JSON_FILE = "wifi_networks.json"


# ================================================
#   Load settings
# ================================================
def load_settings():
    with open(JSON_FILE, encoding="utf-8") as file:
        return json.load(file)


# ================================================
#   Check Wi-Fi interface
# ================================================
def check_wifi_interface(wifi_interface):
    result = subprocess.run(
        ["netsh", "wlan", "show", "interfaces"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    for line in result.stdout.splitlines():
        line = line.strip()

        if line.startswith("名前"):
            interface_name = line.split(":", 1)[1].strip()

            if interface_name == wifi_interface:
                return True

    return False


# ================================================
#   Check Wi-Fi profiles
# ================================================
def check_wifi_profiles(wifi_networks):
    result = subprocess.run(
        ["netsh", "wlan", "show", "profiles"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    missing_profiles = []

    for ssid in wifi_networks:
        if ssid not in result.stdout:
            missing_profiles.append(ssid)

    return missing_profiles


# ================================================
#   Get current SSID
# ================================================
def get_wifi_ssid(wifi_interface):
    result = subprocess.run(
        ["netsh", "wlan", "show", "interfaces"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    target_interface = False

    for line in result.stdout.splitlines():
        line = line.strip()

        if line.startswith("名前"):
            interface_name = line.split(":", 1)[1].strip()
            target_interface = interface_name == wifi_interface
            continue

        if target_interface and line.startswith("SSID"):
            return line.split(":", 1)[1].strip()

    return None


# ================================================
#   Wait for disconnect
# ================================================
def wait_for_disconnect(wifi_interface):
    while get_wifi_ssid(wifi_interface) is not None:
        time.sleep(0.1)


# ================================================
#   Disconnect Wi-Fi
# ================================================
def disconnect_wifi(wifi_interface):
    current_ssid = get_wifi_ssid(wifi_interface)

    if current_ssid is None:
        print("すでにWi-Fiは切断されています。")
        return True

    subprocess.run(
        [
            "netsh",
            "wlan",
            "disconnect",
            f"interface={wifi_interface}",
        ],
        check=True,
    )

    wait_for_disconnect(wifi_interface)

    print(f"{current_ssid} から切断しました。")

    return True


# ================================================
#   Connect Wi-Fi
# ================================================
def connect_wifi(ssid, wifi_interface):
    subprocess.run(
        [
            "netsh",
            "wlan",
            "connect",
            f"name={ssid}",
            f"interface={wifi_interface}",
        ],
        check=True,
    )


# ================================================
#   Switch Wi-Fi
# ================================================
def switch_wifi(ssid, wifi_interface):
    current_ssid = get_wifi_ssid(wifi_interface)

    if current_ssid == ssid:
        print(f"すでに {ssid} に接続されています。")
        return True

    disconnect_wifi(wifi_interface)
    time.sleep(0.5)

    connect_wifi(ssid, wifi_interface)

    time.sleep(0.5)
    current_ssid = get_wifi_ssid(wifi_interface)

    if current_ssid != ssid:
        print("接続に失敗しました。3秒後に再接続します。")
        time.sleep(3)
        connect_wifi(ssid, wifi_interface)
        time.sleep(1)

    current_ssid = get_wifi_ssid(wifi_interface)
    print("Current SSID:", current_ssid)

    return current_ssid == ssid


# ================================================
#   Switch Wi-Fi network
# ================================================
def switch_wifi_network(ssid):
    settings = load_settings()

    wifi_interface = settings["wifi_interface"]
    wifi_networks = settings["wifi_networks"]

    if not check_wifi_interface(wifi_interface):
        print(f'Wi-Fiインターフェイス "{wifi_interface}" が見つかりません。')
        return False

    if ssid not in wifi_networks:
        print(f'Wi-Fiネットワーク "{ssid}" が設定されていません。')
        return False

    missing_profiles = check_wifi_profiles([ssid])

    if missing_profiles:
        print(f'Wi-Fiプロファイル "{ssid}" が見つかりません。')
        return False

    return switch_wifi(ssid, wifi_interface)


# ================================================
#   Main
# ================================================
def main():
    settings = load_settings()

    wifi_interface = settings["wifi_interface"]
    wifi_networks = settings["wifi_networks"]

    if not check_wifi_interface(wifi_interface):
        print(f'Wi-Fiインターフェイス "{wifi_interface}" が見つかりません。')
        input("ENTERを押してください...")
        return

    missing_profiles = check_wifi_profiles(wifi_networks)

    if missing_profiles:
        print("以下のWi-Fiプロファイルが見つかりません。")

        for ssid in missing_profiles:
            print(f"  {ssid}")

        input("ENTERを押してください...")
        return

    current_ssid = get_wifi_ssid(wifi_interface)

    print(f"使用するインターフェイス: {wifi_interface}")
    print(f"現在接続されているネットワーク: {current_ssid}")
    print()

    print("Wi-Fiメニュー")
    print("-" * 40)
    print("0: キャンセル")
    print("1: Wi-Fi切断")

    for number, ssid in enumerate(wifi_networks, start=2):
        print(f"{number}: {ssid}")

    print("-" * 40)

    try:
        number = int(input("番号を入力してください: "))

        if number == 0:
            print("キャンセルしました。")
            return

        if number == 1:
            print()
            print(f"切断するインターフェイス: {wifi_interface}")
            disconnect_wifi(wifi_interface)
            input("ENTERを押してください...")
            return

        ssid = wifi_networks[number - 2]

    except (ValueError, IndexError):
        print("正しい番号を入力してください。")
        return

    print()
    print(f"接続先: {ssid}")

    switch_wifi(ssid, wifi_interface)

    input("ENTERを押してください...")


if __name__ == "__main__":
    main()