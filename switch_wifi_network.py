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
def get_wifi_ssid():
    result = subprocess.run(
        ["netsh", "wlan", "show", "interfaces"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    for line in result.stdout.splitlines():
        line = line.strip()

        if line.startswith("SSID"):
            ssid = line.split(":", 1)[1].strip()
            return ssid

    return None


# ================================================
#   Wait for disconnect
# ================================================
def wait_for_disconnect():
    while get_wifi_ssid() is not None:
        time.sleep(0.1)


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
    current_ssid = get_wifi_ssid()

    if current_ssid == ssid:
        print(f"すでに {ssid} に接続されています。")
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

    wait_for_disconnect()
    time.sleep(0.5)

    connect_wifi(ssid, wifi_interface)

    time.sleep(0.5)
    current_ssid = get_wifi_ssid()

    if current_ssid != ssid:
        print("接続に失敗しました。3秒後に再接続します。")
        time.sleep(3)
        connect_wifi(ssid, wifi_interface)
        time.sleep(1)

    current_ssid = get_wifi_ssid()
    print("Current SSID: ", current_ssid)

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

    current_ssid = get_wifi_ssid()

    print(f"現在接続されているネットワーク: {current_ssid}")
    print()

    print("接続可能なWi-Fiネットワーク")
    print("-" * 40)
    print("0: キャンセル")

    for number, ssid in enumerate(wifi_networks, start=1):
        print(f"{number}: {ssid}")

    print("-" * 40)

    try:
        number = int(input("どのSSIDに接続しますか？ 番号を入力してください: "))

        if number == 0:
            print("キャンセルしました。")
            return
        
        ssid = wifi_networks[number - 1]
    except (ValueError, IndexError):
        print("正しい番号を入力してください。")
        return

    print()
    print(f"接続先: {ssid}")

    switch_wifi(ssid, wifi_interface)

    input("ENTERを押してください...")


if __name__ == "__main__":
    main()