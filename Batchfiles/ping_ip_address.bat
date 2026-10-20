@echo off

set /p ip_address="Enter destination IP address: "

echo.
ping %ip_address%

echo.
pause