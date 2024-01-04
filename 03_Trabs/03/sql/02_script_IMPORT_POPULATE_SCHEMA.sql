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


-- additional information about "client_encoding" in:
-- http://www.postgresql.org/docs/9.3/static/multibyte.html
-- \encoding WIN1250
\encoding UTF8
;




---------------------------------
DELETE FROM TRACK;
---------------------------------
-- Important info about \copy (psql instruction) and copy (sql statement)
-- cf., http://www.postgresql.org/docs/9.3/static/sql-copy.html
-- Do not confuse COPY with the psql instruction \copy.
-- \copy invokes COPY FROM STDIN or COPY TO STDOUT, and then fetches/stores the data in a file accessible to the psql client.
-- Thus, file accessibility and access rights depend on the client rather than the server when \copy is used.
-- 
-- Therefore, given the above information we will use the ~copy psql instruction (no problems with client permissions
--
\COPY track FROM '..\files\z_dataset_JAN_updated.csv' WITH DELIMITER ',' CSV HEADER 




--========================
-- Testing the copyed data
--========================
SELECT tracking_record_id FROM TRACK
LIMIT 40
;
