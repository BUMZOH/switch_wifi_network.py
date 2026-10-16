@echo off

REM ========================================
REM   Settings
REM ========================================
set "WIFI_NAME=TP-Link_B90C_XG"
set "WIFI_INTERFACE=Wi-Fi"

:MENU
cls
echo ========================================
echo   Network Utility
echo ========================================
echo.
echo   1. Connect Wi-Fi Network
echo   2. Disconnect Wi-Fi Network
echo   3. Show Wi-Fi Interfaces
echo   4. Show Wi-Fi Profiles
echo   5. Show IP Configuration
echo   6. Open Network Connections
echo   0. Exit
echo.
echo ========================================
echo.

set /p choice=Select: 

if "%choice%"=="1" goto CONNECT
if "%choice%"=="2" goto DISCONNECT
if "%choice%"=="3" goto INTERFACE
if "%choice%"=="4" goto PROFILE
if "%choice%"=="5" goto IPCONFIG
if "%choice%"=="6" goto NETWORK
if "%choice%"=="0" goto EXIT

goto MENU


:CONNECT
cls
echo Connecting to Wi-Fi Network...
echo.

netsh wlan connect name="%WIFI_NAME%" interface="%WIFI_INTERFACE%"

timeout /t 3 /nobreak >nul

echo.
netsh wlan show interfaces

pause
goto MENU


:DISCONNECT
cls
echo Disconnecting Wi-Fi Network...
echo.

netsh wlan disconnect interface="%WIFI_INTERFACE%"

timeout /t 3 /nobreak >nul

echo.
netsh wlan show interfaces

pause
goto MENU


:INTERFACE
cls
netsh wlan show interfaces

pause
goto MENU


:PROFILE
cls
netsh wlan show profiles

pause
goto MENU


:IPCONFIG
cls
ipconfig

pause
goto MENU


:NETWORK
start "" ncpa.cpl
goto MENU


:EXIT
exit