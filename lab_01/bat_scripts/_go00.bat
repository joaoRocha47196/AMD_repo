@ECHO OFF

set psqlPath="C:\Program Files\PostgreSQL\16\bin\psql.exe"

:: Database, Username, Password, and Port
SET dataBase=postgres
SET userName=postgres
SET passWord=password1234  :: Replace with your password
SET portNumber=5432
SET hostName=127.0.0.1

:: Set the PGPASSWORD environment variable for this session
SET PGPASSWORD=%passWord%

:: Execute SQL commands
echo Running commands...
%psqlPath% -h %hostName% -U %userName% -d %dataBase% -p %portNumber% -a -c "\set dataBase db_operational; DROP DATABASE IF EXISTS :dataBase; CREATE DATABASE :dataBase TEMPLATE = my_db;"

ECHO Operation Completed.
PAUSE
