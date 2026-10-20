@echo off

set /p interface="Enter Wi-Fi interface name: "

echo.
netsh wlan disconnect interface="%interface%"

echo.
pause