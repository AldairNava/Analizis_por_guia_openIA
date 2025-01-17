@echo on
taskkill /F /im py.exe
taskkill /F /im py.exe
taskkill /F /im py.exe
taskkill /F /im py.exe

powershell -Command "Start-Process powershell -ArgumentList '-Command', 'python C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Analisis_Masivo_guia\main.py'"