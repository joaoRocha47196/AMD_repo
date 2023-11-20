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
-- DELETE DATA FROM TABLES
--==========================
DELETE FROM DIAGNOSIS;
DELETE FROM LENSE;
DELETE FROM Appointment;
DELETE FROM Disease;
DELETE FROM Doctor;
DELETE FROM Patient;
DELETE FROM OcularAge;
DELETE FROM LensHardness;
DELETE FROM TearRate;

--==========================
-- POPULATE TABLES
--==========================

--############
-- Tabelas de Mapeamento
--############
INSERT INTO OcularAge (MinLimit, MaxLimit, Val) 
VALUES 
    (0, 30, 'young'),
    (30, 45, 'pre-presbyopic'),
    (45, 99, 'presbyopic');

INSERT INTO LensHardness (MinLimit, MaxLimit, Val) 
VALUES 
    (0, 0.1, 'none'),
    (0.1, 0.3, 'soft'),
    (0.3, 0.99, 'hard');

INSERT INTO TearRate (MinLimit, MaxLimit, Val) 
VALUES
    (0, 0.5, 'reduced'),
    (0.5, 1.0, 'normal');


--############
-- Tabelas de Dados
--############
INSERT INTO Patient (PatientID, FirstName, LastName, BirthDate, ContactInfo) 
VALUES 
    (1, 'João', 'Silva', '2005-01-01', 'joao@example.com'),
    (2, 'Ana', 'Santos', '2004-02-02', 'ana@example.com'),
    (3, 'Miguel', 'Oliveira', '1997-03-03', 'miguel@example.com'),
    (4, 'Sofia', 'Costa', '1998-04-04', 'sofia@example.com'),
    (5, 'Francisco', 'Martins', '1998-05-05', 'francisco@example.com'),
    (6, 'Mariana', 'Ferreira', '1980-06-06', 'mariana@example.com'),
    (7, 'Diogo', 'Pereira', '1980-07-07', 'diogo@example.com'),
    (8, 'Beatriz', 'Rocha', '1980-08-08', 'beatriz@example.com'),
    (9, 'Lucas', 'Fernandes', '1980-09-09', 'lucas@example.com'),
    (10, 'Matilde', 'Gonçalves', '1980-10-10', 'matilde@example.com'),
    (11, 'Rafael', 'Cardoso', '1980-11-11', 'rafael@example.com'),
    (12, 'Carolina', 'Ribeiro', '1960-12-12', 'carolina@example.com'),
    (13, 'Gabriel', 'Pinto', '1960-01-13', 'gabriel@example.com'),
    (14, 'Leonor', 'Carvalho', '1960-02-14', 'leonor@example.com'),
    (15, 'Simão', 'Marques', '1960-03-15', 'simao@example.com'),
    (16, 'Madalena', 'Teixeira', '1960-04-16', 'madalena@example.com');


INSERT INTO Doctor (DoctorID, FirstName, LastName, Specialty, ContactInfo) 
VALUES 
    (1, 'Dr. Doctor', '1', 'Ophthalmology', 'doctor1@example.com'),
    (2, 'Dr. Doctor', '2', 'Ophthalmology', 'doctor2@example.com');

INSERT INTO Disease (DiseaseID) 
VALUES 
    ('astigmatic'),
    ('myope'),
    ('hypermetrope');

INSERT INTO Appointment (AppointmentID, PatientID, DoctorID, VisitDate, TearRate) 
VALUES 
    (1, 1, 1, '2023-01-01 10:00:00', 0.6),
    (2, 2, 2, '2023-01-02 11:00:00', 0.7),
    (3, 3, 1, '2023-01-03 12:00:00', 0.2),
    (4, 4, 2, '2023-01-04 13:00:00', 0.8),
    (5, 5, 1, '2023-01-05 14:00:00', 0.3),
    (6, 6, 2, '2023-01-06 15:00:00', 0.3),
    (7, 7, 1, '2023-01-07 16:00:00', 0.9),
    (8, 8, 2, '2023-01-08 17:00:00', 0.1),
    (9, 9, 1, '2023-01-09 18:00:00', 0.58),
    (10, 10, 2, '2023-01-10 19:00:00', 0.55),
    (11, 11, 1, '2023-01-11 20:00:00', 0.2),
    (12, 12, 2, '2023-01-12 21:00:00', 0.1),
    (13, 13, 1, '2023-01-13 22:00:00', 0.7),
    (14, 14, 2, '2023-01-14 23:00:00', 0.6),
    (15, 15, 1, '2023-01-15 00:00:00', 0.8),
    (16, 16, 2, '2023-01-16 01:00:00', 0.9);

INSERT INTO DIAGNOSIS (AppointmentID, DiseaseID) 
VALUES 
    (1, 'myope'),
    (1, 'astigmatic'),
    (2, 'myope'),
    (3, 'hypermetrope'),
    (3, 'astigmatic'),
    (4, 'hypermetrope'),
    (5, 'hypermetrope'),
    (6, 'myope'),
    (6, 'astigmatic'),
    (7, 'myope'),
    (7, 'astigmatic'),
    (8, 'hypermetrope'),
    (8, 'astigmatic'),
    (9, 'hypermetrope'),
    (9, 'astigmatic'),
    (10, 'hypermetrope'),
    (11, 'hypermetrope'),
    (12, 'myope'),
    (12, 'astigmatic'),
    (13, 'myope'),
    (13, 'astigmatic'),
    (14, 'myope'),
    (15, 'hypermetrope'),
    (15, 'astigmatic'),
    (16, 'hypermetrope');

INSERT INTO LENSE (AppointmentID, LensHardness)
VALUES 
    (1, 0.6),
    (2, 0.2),
    (3, 0.02),
    (4, 0.3),
    (5, 0.03),
    (6, 0.05),
    (7, 0.9),
    (8, 0.01),
    (9, 0.05),
    (10, 0.25),
    (11, 0.02),
    (12, 0.05),
    (13, 0.7),
    (14, 0.2),
    (15, 0.05),
    (16, 0.2);

