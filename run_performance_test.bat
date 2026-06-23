@echo off
setlocal

set ROOT=%~dp0

echo =====================================
echo LEVANTANDO SPRING PETCLINIC
echo =====================================

cd /d "%ROOT%spring-petclinic"

start "Spring PetClinic" cmd /k "cd /d %ROOT%spring-petclinic && mvnw spring-boot:run"

echo Esperando que Spring Boot inicie...

:wait
timeout /t 5 > nul

curl -s http://localhost:8080 > nul

if %errorlevel% neq 0 (
    echo Esperando servidor...
    goto wait
)

echo Spring Boot esta listo!


echo =====================================
echo EJECUTANDO K6
echo =====================================

cd /d "%ROOT%k6-env"

if not exist results mkdir results


k6 run ^
--out json=results\resultado.json ^
"%ROOT%k6-env\Scripts\pet_clinic_test.js"


if %ERRORLEVEL% NEQ 0 (
    echo Error ejecutando k6
    pause
    exit /b 1
)


echo =====================================
echo GENERANDO REPORTE
echo =====================================

"%ROOT%k6-env\Scripts\python.exe" generar_reporte.py

echo =====================================
echo FINALIZADO
echo =====================================

pause