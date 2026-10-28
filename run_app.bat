@echo off
title MoodBeat AI - Running on PC & Mobile
echo =================================================================
echo             MOODBEAT AI - SMART EMOTION MUSIC PLAYER
echo =================================================================
echo.
echo [PC Access]:     http://localhost:5000
echo [Mobile Access]: http://192.168.1.9:5000
echo.
echo (Make sure your mobile phone is connected to the same Wi-Fi!)
echo.
echo Opening browser...
start http://localhost:5000
python app.py
pause
