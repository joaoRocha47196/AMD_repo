
with the code bellow complete the “create view” code in order to
obtain the output as presented in the bottom of the file (cf., below the [OUT] tag)

now complete this psql script where complete the “create view” code in order to
obtain the output as presented in the bottom of the file below the [OUT] tag :  



1.

c)
.\_go.bat .\02_script_POPULATE_SCHEMA.txt
You are now connected to database "db_operational" as user "postgres".
DELETE 3
DELETE 3
DELETE 4
DELETE 3
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1

1 e)
CREATE VIEW
 vc1 | vc2 |    vc3
-----+-----+------------
 111 |   1 | 2012-01-31
 111 |   1 | 2012-02-28
 222 |   2 | 2012-03-31
(3 rows)

2 c)\COPY (SELECT * FROM v1) TO :filePath WITH CSV HEADER;
.\_go.bat .\30_script_EXPORT_DATA.txt
You are now connected to database "db_operational" as user "postgres".
COPY 3