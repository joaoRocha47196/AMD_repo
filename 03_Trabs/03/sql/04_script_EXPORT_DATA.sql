--#############
--# Paulo Trigo
--#############


--==============
-- DB connection
--==============
\set dataBase db_e_commerce_project_b
;
\set userName postgres
;
\connect :dataBase :userName
;
--==========================
--==========================


\encoding UTF8
;


--==========================
-- [PRS: ADAPT]
-- the file path where to write the data
\set filePath './z_dataset_OUT_result.txt'
--==========================



--==============================
-- export to text data file
--==============================
-- the COPY statement executes wihin server context and thus uses postgreSQL user's credentials
-- very important: "\o" psdql statement redirects the STDOUT into a file path - this way it uses client credentials intead of server credentials
\o :filePath

--==============================
-- the COPY PostgreSQL statement
-- (for detailed information see: http://www.postgresql.org/docs/9.6/static/sql-copy.html)

COPY ( SELECT cookie_id, product_gui FROM v_export ORDER BY cookie_id )
TO STDOUT  -- will write to redirected STDOUT (value of :filePath; cf., statement above)
-- WITH ( FORMAT CSV, HEADER TRUE, FORCE_QUOTE (vc1, vc3), QUOTE '"', DELIMITER E'\t' )
-- WITH ( FORMAT CSV, HEADER TRUE, DELIMITER ';' )
WITH ( FORMAT CSV, HEADER FALSE, DELIMITER ';' )
;

--==============================




