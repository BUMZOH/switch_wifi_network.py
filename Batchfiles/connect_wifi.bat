@echo off

set /p name="Enter Wi-Fi profile name: "
set /p interface="Enter Wi-Fi interface name: "

echo.
netsh wlan connect name="%name%" interface="%interface%"

echo.
pause