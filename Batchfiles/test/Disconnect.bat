netsh wlan disconnect interface="Wi-Fi 2"

timeout /t 3 /nobreak >nul

netsh wlan show interfaces

pause