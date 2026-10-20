@echo off

cd /d "%~dp0"

set /p interface="Enter Wi-Fi interface name: "

echo.
netsh wlan add profile filename="wifi_profile.xml" interface="%interface%"

echo.
pause