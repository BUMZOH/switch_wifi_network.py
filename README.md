# Wi-Fi Network Switcher

WindowsのWi-Fi接続先を、Pythonから簡単に切り替えるためのツールです。

Windows標準の `netsh`
コマンドを利用して、JSONファイルに登録したWi-Fiネットワークへ接続します。

単体のCLIツールとして利用できるほか、他のPythonプログラムから
`switch_wifi_network()` をインポートして利用することもできます。

## 主な機能

-   JSONファイルによるWi-Fiインターフェイスと接続先の設定
-   起動時のWi-Fiインターフェイス存在確認
-   登録済みWi-Fiプロファイルの確認
-   現在接続中のSSID表示
-   メニューから接続先SSIDを選択
-   Wi-Fi切り替え時の自動再接続
-   他のPythonプログラムから関数として利用可能
-   接続結果を `True` / `False` で取得可能

## 動作環境

-   Windows
-   Python 3
-   Windowsの `netsh wlan` コマンドが利用できること
-   接続対象のWi-FiプロファイルがWindowsに登録済みであること

外部Pythonパッケージは使用していません。

## ファイル構成

``` text
.
├── switch_wifi_network.py
├── template_wifi_networks.json
├── wifi_networks.json
└── .gitignore
```

`wifi_networks.json` は使用するPCごとに内容が異なるローカル設定ファイルのため、
Gitの管理対象には含めません。

GitHubに含まれている `template_wifi_networks.json` をコピーして、
`wifi_networks.json` という名前で保存し、使用環境に合わせて内容を編集してください。

`switch_wifi_network.py` と作成した `wifi_networks.json`
は同じフォルダに配置してください。

## 設定

### wifi_networks.json の準備

最初に `template_wifi_networks.json` をコピーして、
ファイル名を `wifi_networks.json` に変更します。

```text
template_wifi_networks.json
        ↓ コピー
wifi_networks.json
```

次に、作成した `wifi_networks.json` のWi-Fiインターフェイス名と
接続可能なWi-Fiネットワークを使用環境に合わせて設定します。

`wifi_networks.json` は `.gitignore` に登録されているため、
PC固有の設定を変更してもGitの管理対象にはなりません。

``` json
{
    "wifi_interface": "Wi-Fi",
    "wifi_networks": [
        "SSID_1",
        "SSID_2"
    ]
}
```

### wifi_interface

Windowsで使用するWi-Fiインターフェイス名を指定します。

例：

``` json
"wifi_interface": "Wi-Fi"
```

インターフェイス名は、コマンドプロンプトで次のコマンドを実行して確認できます。

``` bat
netsh wlan show interfaces
```

PCによっては `Wi-Fi 2` などの名前になっている場合があります。

### wifi_networks

切り替え先として使用するWi-Fiネットワーク名をリストで登録します。

``` json
"wifi_networks": [
    "SSID_1",
    "SSID_2"
]
```

対象ネットワークは、あらかじめWindowsにWi-Fiプロファイルとして
登録されている必要があります。

登録済みプロファイルは次のコマンドで確認できます。

``` bat
netsh wlan show profiles
```

## 単体で使用する

コマンドプロンプトなどから実行します。

``` bat
python switch_wifi_network.py
```

起動すると、現在接続されているネットワークと、
JSONに登録されている接続先が表示されます。

``` text
現在接続されているネットワーク: TP-Link_B90C_XG

接続可能なWi-Fiネットワーク
----------------------------------------
0: キャンセル
1: TP-Link_B90C_XG
2: TP-Link_B8C2_PLC
----------------------------------------
どのSSIDに接続しますか？ 番号を入力してください:
```

接続したいSSIDの番号を入力してください。

`0` を入力するとキャンセルします。

## 他のPythonプログラムから使用する

`switch_wifi_network.py` はモジュールとしてインポートできます。

``` python
from switch_wifi_network import switch_wifi_network


success = switch_wifi_network("TP-Link_B8C2_PLC")

if success:
    print("Wi-Fi切り替え成功")
else:
    print("Wi-Fi切り替え失敗")
```

### 関数

``` python
switch_wifi_network(ssid)
```

#### 引数

`ssid`

接続先のWi-Fiネットワーク名を文字列で指定します。

``` python
switch_wifi_network("TP-Link_B8C2_PLC")
```

指定するSSIDは `wifi_networks.json` の `wifi_networks` に
登録されている必要があります。

#### 戻り値

  戻り値    意味
  --------- ------------------------------------------
  `True`    指定したSSIDへの接続に成功
  `False`   接続できなかった、または設定に問題がある

すでに指定したSSIDへ接続されている場合も `True` を返します。

## 外部利用時の処理

`switch_wifi_network()` を呼び出すと、次の順番で確認・接続を行います。

``` text
switch_wifi_network(ssid)
        ↓
JSON設定を読み込む
        ↓
Wi-Fiインターフェイスが存在するか確認
        ↓
SSIDがJSONに登録されているか確認
        ↓
Wi-Fiプロファイルが存在するか確認
        ↓
現在のSSIDを確認
        ↓
Wi-Fiを切断
        ↓
指定SSIDへ接続
        ↓
接続確認
        ↓
失敗時は3秒待って再接続
        ↓
最終SSIDを確認
        ↓
True / False を返す
```

## 自動再接続

Wi-Fi切り替え直後は、環境によって1回目の接続に失敗する場合があります。

本ツールでは最初の接続後にSSIDを確認し、指定したSSIDへ
接続できていない場合は3秒待ってから再接続します。

これにより、一時的な接続失敗に対応します。

## 起動時のチェック

単体実行時は、SSID選択メニューを表示する前に次の確認を行います。

1.  JSONで指定したWi-Fiインターフェイスが存在するか
2.  JSONに登録したWi-FiプロファイルがWindowsに存在するか

問題がある場合はメッセージを表示し、Wi-Fi切り替え処理へ進みません。

## 使用している主なnetshコマンド

### Wi-Fiインターフェイス確認

``` bat
netsh wlan show interfaces
```

### Wi-Fiプロファイル確認

``` bat
netsh wlan show profiles
```

### Wi-Fi切断

``` bat
netsh wlan disconnect interface="Wi-Fi"
```

### Wi-Fi接続

``` bat
netsh wlan connect name="SSID" interface="Wi-Fi"
```

## 注意事項

-   Windows専用です。
-   接続対象SSIDはWindowsへ事前登録してください。
-   `wifi_interface`
    は実際のWindowsのインターフェイス名と一致させてください。
-   `template_wifi_networks.json` をコピーして `wifi_networks.json`
    を作成し、使用環境に合わせて設定してください。
-   `wifi_networks.json` は `switch_wifi_network.py`
    から読み込める場所に配置してください。
-   `wifi_networks.json` はPC固有の設定ファイルのため、Git管理対象には含めません。
-   Wi-FiアダプタやPCを変更した場合は、インターフェイス名を再確認してください。

## 設計方針

Wi-Fi切り替え処理の詳細を `switch_wifi_network.py` にまとめ、
利用側のプログラムでは次のような単純な呼び出しだけで使用できる構成にしています。

``` python
success = switch_wifi_network("TP-Link_B8C2_PLC")
```

利用側は `netsh` のコマンドやWi-Fiインターフェイス名、
再接続処理などを意識する必要がありません。

また、

``` python
if __name__ == "__main__":
    main()
```

によって、同じファイルを単体CLIツールとしても、
他のPythonプログラムから利用するモジュールとしても使用できます。
