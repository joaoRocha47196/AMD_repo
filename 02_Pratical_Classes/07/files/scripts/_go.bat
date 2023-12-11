@ECHO OFF

:: [PTS: ADAPT]
set psqlPath="C:\Program Files\PostgreSQL\16\bin\psql.exe"

:: Database, Username, Password, and Port
SET dataBase=my_db
SET userName=postgres
SET passWord=password1234
SET portNumber=5432
SET hostName=127.0.0.1

:: Set the password environment variable
SET PGPASSWORD=%passWord%

:: Connect to database and execute the instructions within psqlFile
%psqlPath% -h localhost -p %portNumber% -d %dataBase% -U %userName% -f %1