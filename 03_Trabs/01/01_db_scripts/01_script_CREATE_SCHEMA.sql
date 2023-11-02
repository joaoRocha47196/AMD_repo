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
-- DELETE TABLES
--==========================
DROP TABLE IF EXISTS DIAGNOSIS CASCADE;
DROP TABLE IF EXISTS LENSE CASCADE;
DROP TABLE IF EXISTS Appointment CASCADE;
DROP TABLE IF EXISTS Disease CASCADE;
DROP TABLE IF EXISTS Doctor CASCADE;
DROP TABLE IF EXISTS Patient CASCADE;
DROP TABLE IF EXISTS OcularAge CASCADE;
DROP TABLE IF EXISTS LensHardness CASCADE;
DROP TABLE IF EXISTS TearRate CASCADE;


--==========================
-- CREATE TABLES
--==========================
--############
-- Tabelas de Dados
--############
CREATE TABLE Patient (
    PatientID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    BirthDate DATE NOT NULL,
    ContactInfo VARCHAR(50) NOT NULL
);

CREATE TABLE Doctor (
    DoctorID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Specialty VARCHAR(50) NOT NULL,
    ContactInfo VARCHAR(50) NOT NULL
);

CREATE TABLE Disease (
    DiseaseID VARCHAR(50) PRIMARY KEY -- DisiaseID is the diseaeName
);

CREATE TABLE Appointment (
    AppointmentID INT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    VisitDate TIMESTAMP NOT NULL,
    TearRate FLOAT NOT NULL,   
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
);

CREATE TABLE DIAGNOSIS ( -- Relates Appointment with Disease
    AppointmentID INT,
    DiseaseID VARCHAR(50),
    PRIMARY KEY (AppointmentID, DiseaseID),
    FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID),
    FOREIGN KEY (DiseaseID) REFERENCES Disease(DiseaseID)
);

CREATE TABLE LENSE (
    AppointmentID INT,
    LensHardness FLOAT,
    FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID)
);

--############
-- Tabelas de Mapeamento
--############
CREATE TABLE OcularAge (  
    MaxLimit INT NOT NULL,
    MinLimit INT NOT NULL,
    Val VARCHAR(50) NOT NULL,
    PRIMARY KEY (MaxLimit, MinLimit)
);

CREATE TABLE LensHardness (
    MaxLimit FLOAT NOT NULL,
    MinLimit FLOAT NOT NULL,
    Val VARCHAR(50) NOT NULL,
    PRIMARY KEY (MaxLimit, MinLimit)
);

CREATE TABLE TearRate (
    MaxLimit FLOAT NOT NULL,
    MinLimit FLOAT NOT NULL,
    Val VARCHAR(50) NOT NULL,
    PRIMARY KEY (MaxLimit, MinLimit)
);
