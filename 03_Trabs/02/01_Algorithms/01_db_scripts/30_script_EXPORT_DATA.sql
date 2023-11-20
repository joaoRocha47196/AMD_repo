--#############
--# AMD GXX
--#############

--==============
-- DB connection
--==============
\set dataBase db_medknow
\set userName postgres

\connect :dataBase :userName

--==========================
-- GENERATE CSV FILE
--==========================
\COPY (SELECT VC2 as age, VC3 as prescription, VC4 as astigmatic, VC5 as tear_rate, VC6 as lenses FROM view_dataset) TO '../02_gen_files/view_export.tab' WITH CSV HEADER DELIMITER ';';

--==========================
-- GENERATE TAB FILE
--==========================
\COPY (SELECT VC2, VC3, VC4, VC5, VC6 FROM view_export) TO '../02_gen_files/view_export.tab' with delimiter E'\t' null as ';'                