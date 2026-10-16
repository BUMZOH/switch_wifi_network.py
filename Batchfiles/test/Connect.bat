netsh wlan connect name="TP-Link_B90C_XG" interface="Wi-Fi 2"

timeout /t 3 /nobreak >nul

netsh wlan show interfaces

pause