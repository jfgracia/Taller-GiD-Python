@ECHO OFF

rem OutputFile: %2\%1.log
rem ErrorFile: %2\%1.err

set PYTHON_PATH=C:\Program Files\GiD\GiD 17.1.1d\scripts\tohil\python\python
set SOURCE_PATH=C:\Users\jfgracia\Documents\Taller-GiD-Python\main.py

rem Se reciben 3 argumentos
rem %1 Es el nombre del documento
rem %2 Es el directorio donde esta el documento
rem %3 Es el directiorio donde esta el Problemtype

rem Si existen documentos de la ejecucion anterior entonces borrarlos
del %2\%1.log
del %2\%1.post.res
del %2\%1.err

rem Ejecutar la rutina, mandar argumento directorio y nombre del documento
rem GiD viene con su propia distribucion de Python
rem Hay que referirse a la ayuda en linea para instalar los modulos extras
rem https://gidsimulation.atlassian.net/wiki/spaces/GCM/overview

%PYTHON_PATH% %SOURCE_PATH% %2\%1 > %2\%1.log

