--#############
--# AMD GXX
--#############



--==============
-- DB connection
--==============
\set dataBase db_medknow
;
\set userName postgres
;
\connect :dataBase :userName
;

--==========================
-- DROP VIEWS
--==========================
DROP VIEW IF EXISTS view_export;
DROP VIEW IF EXISTS view_attrType;
DROP VIEW IF EXISTS view_class;
DROP VIEW IF EXISTS view_dataset;

--==========================
-- DATASET VIEW
--==========================
CREATE VIEW view_dataset AS
SELECT 
    4 AS ordering,
    a.PatientID as VC1,
    (
        SELECT oa.Val
        FROM OcularAge oa
        WHERE (DATE_PART('year', current_date) - DATE_PART('year', p.BirthDate)) BETWEEN oa.MinLimit AND oa.MaxLimit
        LIMIT 1
    ) AS VC2,

    (
        SELECT d.DiseaseID
        WHERE d.DiseaseID != 'astigmatic'
    ) AS VC3,
    CASE 
        WHEN EXISTS (
            SELECT 'astigmatic' 
            FROM diagnosis d2
            WHERE d2.AppointmentID = a.AppointmentID AND d2.DiseaseID = 'astigmatic' 
        ) THEN 'yes'
        ELSE 'no'
    END AS VC4,

    (
        SELECT t.Val
        FROM TearRate t
        WHERE a.TearRate BETWEEN t.MinLimit AND t.MaxLimit
        LIMIT 1
    ) AS VC5,

    (
        SELECT lh.Val
        FROM LensHardness lh 
        WHERE l.LensHardness BETWEEN lh.MinLimit AND lh.MaxLimit
        LIMIT 1
    ) AS VC6
FROM 
    Patient p
JOIN 
    Appointment a ON p.PatientID = a.PatientID
LEFT JOIN 
    diagnosis d ON a.AppointmentID = d.AppointmentID
LEFT JOIN
    lense l ON a.AppointmentID = l.AppointmentID
WHERE 
    d.DiseaseID IN ('myope', 'hypermetrope') -- To avoid duplicate
ORDER BY 
    VC1;
 
--==========================
-- DOMAIN VIEW
--==========================
CREATE OR REPLACE VIEW view_domain AS
SELECT 
    2 AS ordering,
    'pre-presbyopic presbyopic young'::text AS VC2,
    'hypermetrope myope'::text AS VC3,
    'no yes'::text AS VC4,
    'normal reduced'::text AS VC5,
    'hard none soft'::text AS VC6;

--==========================
-- ATRIBUT VIEW
--==========================
CREATE OR REPLACE VIEW view_attrType AS
SELECT 
    1 AS ordering,
    'age'::text AS VC2,
    'prescription'::text AS VC3,
    'astigmatic'::text AS VC4,
    'tear_rate'::text AS VC5,
    'lenses'::text AS VC6;

--==========================
-- CLASS VIEW
--==========================
CREATE OR REPLACE VIEW view_class AS
SELECT 
    3 AS ordering,
    ''::text AS VC2,
    ''::text AS VC3,
    ''::text AS VC4,
    ''::text AS VC5,
    'class'::text AS VC6;

--==========================
-- EXPORT VIEW
--==========================
CREATE OR REPLACE VIEW view_export AS
SELECT ordering, VC2, VC3, VC4, VC5,VC6
FROM (
    SELECT ordering, VC2, VC3, VC4, VC5, VC6 FROM view_attrType
    UNION ALL
    SELECT ordering, VC2, VC3, VC4, VC5, VC6 FROM view_domain
    UNION ALL
    SELECT ordering, VC2, VC3, VC4, VC5, VC6 FROM view_class
    UNION ALL
    SELECT ordering, VC2, VC3, VC4, VC5, VC6 FROM view_dataset
) AS combined_views
ORDER BY ordering;

SELECT * FROM view_export;