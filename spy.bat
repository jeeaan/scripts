REM Criar a pasta shot:
REM C:\Users\<User Profile folder name>\Pictures\shot\
REM Runner do script a cada inicialização do sistema:
REM C:\Users\<User Profile folder name>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
REM A cada 12 segundos tirar uma foto, quando chegar (se chegar) em 100.000 vai parar o loop

@echo off
nircmd.exe loop 100000 12000 savescreenshot C:\Users\<User Profile folder name>\Pictures\shot\~$currdate.MM-dd-yyyy$-~$currtime.HH_mm_ss$