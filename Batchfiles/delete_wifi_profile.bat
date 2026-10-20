@echo off

set /p profile="Enter Wi-Fi profile name: "
set /p interface="Enter Wi-Fi interface name: "

echo.
netsh wlan delete profile name="%profile%" interface="%interface%"

echo.
pause