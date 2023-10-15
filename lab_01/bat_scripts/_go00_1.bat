@ECHO OFF

set psqlPath="C:\Program Files\PostgreSQL\16\bin\psql.exe"

:: Database, Username, Password, and Port
SET dataBase=postgres
SET userName=postgres
:: Replace with your password
SET passWord=password12234
SET portNumber=5432
SET hostName=127.0.0.1

:: Set the PGPASSWORD environment variable for automatic authentication
SET PGPASSWORD=%passWord%

:: Execute SQL commands
echo Running commands...
%psqlPath% -h %hostName% -U %userName% -d %dataBase% -p %portNumber%


echo Operation Completed.
PAUSE
