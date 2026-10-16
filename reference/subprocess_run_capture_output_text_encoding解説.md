# Python `subprocess.run()` の `capture_output`・`text`・`encoding` 解説

## 1. はじめに

PythonからWindowsのコマンドを実行するときは、`subprocess`
モジュールを利用できます。

今回の例では、`netsh` コマンドをPythonから実行しています。

``` python
result = subprocess.run(
    ["netsh", "wlan", "show", "interfaces"],
    capture_output=True,
    text=True,
    encoding="utf-8",
)
```

このコードは、簡単に言うと次の処理を行っています。

> `netsh` を実行し、その実行結果をPythonから文字列として受け取る。

特に重要なのが、次の3つのオプションです。

-   `capture_output=True`
-   `text=True`
-   `encoding="utf-8"`

------------------------------------------------------------------------

## 2. `capture_output=True`

### 役割

`capture_output=True` は、

> 外部コマンドの実行結果をPython側で受け取る

ための指定です。

例えば、次のように実行した場合、

``` python
subprocess.run(
    ["netsh", "wlan", "show", "interfaces"],
)
```

`netsh` の実行結果は、そのままコンソールに表示されます。

一方、

``` python
result = subprocess.run(
    ["netsh", "wlan", "show", "interfaces"],
    capture_output=True,
)
```

とすると、実行結果をPython側で取得できます。

通常の出力は、

``` python
result.stdout
```

エラー出力は、

``` python
result.stderr
```

に格納されます。

イメージは次のとおりです。

``` text
netshを実行
    ↓
コマンドの出力
    ↓
capture_output=True
    ↓
Pythonが出力を受け取る
    ↓
result.stdout
```

### 今回のプログラムで必要な理由

今回のコードでは、取得した結果を、

``` python
for line in result.stdout.splitlines():
```

のようにPython側で解析しています。

そのため、コンソールへ直接表示させるのではなく、 `capture_output=True`
で結果をPythonへ取り込む必要があります。

------------------------------------------------------------------------

## 3. `stdout` と `stderr`

`capture_output=True` を指定すると、主に次の2つを利用できます。

  属性              内容
  ----------------- ----------------------------
  `result.stdout`   通常の実行結果
  `result.stderr`   エラーとして出力された内容

例えば、

``` python
print(result.stdout)
print(result.stderr)
```

とすれば、それぞれの内容を確認できます。

------------------------------------------------------------------------

## 4. `text=True`

### 役割

`text=True` は、

> コマンドから受け取ったデータをPythonの文字列 `str` として扱う

ための指定です。

外部プログラムとのやり取りでは、元々のデータはバイト列として扱われます。

`text=True` を使用しない場合、例えば次のような `bytes`
データになります。

``` python
b'...'
```

`text=True` を指定すると、

``` python
'...'
```

という通常のPython文字列として扱えます。

そのため、

``` python
result.stdout.splitlines()
```

や、

``` python
line.startswith("名前")
```

などの文字列処理を簡単に行えます。

------------------------------------------------------------------------

## 5. `encoding="utf-8"`

### 役割

`encoding` は、

> バイト列を文字列へ変換するときに使用する文字コード

を指定します。

今回の場合は、

``` python
encoding="utf-8"
```

なので、UTF-8として文字列へ変換します。

`text=True` と `encoding`
は関連が深く、次のように考えると分かりやすいです。

``` text
外部コマンドからデータを取得
    ↓
元はバイト列
    ↓
encoding="utf-8"
    ↓
UTF-8として変換
    ↓
text=True
    ↓
Pythonの文字列として利用
```

------------------------------------------------------------------------

## 6. 3つのオプションをまとめる

``` python
result = subprocess.run(
    ["netsh", "wlan", "show", "interfaces"],
    capture_output=True,
    text=True,
    encoding="utf-8",
)
```

それぞれの役割は次のとおりです。

  オプション              意味
  ----------------------- --------------------------------------------
  `capture_output=True`   コマンドの出力をPythonで受け取る
  `text=True`             受け取った出力を文字列として扱う
  `encoding="utf-8"`      文字列へ変換するときの文字コードを指定する

全体の流れは、

``` text
netshを実行
    ↓
capture_output=True
    ↓
実行結果をPythonで取得
    ↓
encoding="utf-8"
    ↓
指定した文字コードで変換
    ↓
text=True
    ↓
Pythonの文字列として扱う
    ↓
result.stdout
```

と考えることができます。

------------------------------------------------------------------------

## 7. 実用上の覚え方

細かい内部動作よりも、まずは次のように覚えておけば十分です。

``` python
result = subprocess.run(
    command,
    capture_output=True,  # 実行結果をPythonで取得
    text=True,            # 文字列として取得
    encoding="utf-8",     # 文字コードを指定
)
```

特に、

> `capture_output=True` =
> 画面に出すだけではなく、Pythonで実行結果を使いたい

と覚えると分かりやすいです。

------------------------------------------------------------------------

## 8. `capture_output=True` の内部的な意味

少し発展的な内容ですが、

``` python
capture_output=True
```

は、概念的には次の2つをまとめて指定する便利な書き方です。

``` python
stdout=subprocess.PIPE,
stderr=subprocess.PIPE,
```

つまり、

``` python
result = subprocess.run(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
```

のような指定を簡潔に書けます。

通常は `capture_output=True` の方が読みやすいため、
単純に標準出力と標準エラー出力を取得したい場合はこちらが便利です。

------------------------------------------------------------------------

## 9. 今回のコードでの利用例

``` python
result = subprocess.run(
    ["netsh", "wlan", "show", "interfaces"],
    capture_output=True,
    text=True,
    encoding="utf-8",
)

for line in result.stdout.splitlines():
    line = line.strip()

    if line.startswith("名前"):
        print(line)
```

処理の流れは、

1.  Pythonから`netsh wlan show interfaces`を実行する
2.  `capture_output=True`で出力をPythonへ取り込む
3.  `text=True`で文字列として扱う
4.  `encoding="utf-8"`で文字コードを指定する
5.  `result.stdout`から実行結果を取得する
6.  `splitlines()`で1行ずつ解析する

となります。

------------------------------------------------------------------------

## 10. まとめ

今回の3つは、PythonからWindowsコマンドを実行して、
その結果をプログラム内で利用するときによく使う組み合わせです。

``` python
capture_output=True
text=True
encoding="utf-8"
```

まずは、

> **コマンドを実行 → 結果を取得 → Pythonの文字列として処理**

するための設定、と理解しておけば十分です。
