EXP-5

-- ── 1. INITIAL TABLE CREATION & POPULATION ────────────

CREATE TABLE Department (
    dept_id INT PRIMARY KEY, 
    dept_name VARCHAR2(30)
);

CREATE TABLE Student_Basic (
    student_id INT PRIMARY KEY, 
    name VARCHAR2(50), 
    cgpa NUMBER(4,2)
);

INSERT INTO Department VALUES (1, 'CSE');
INSERT INTO Department VALUES (2, 'ECE');

INSERT INTO Student_Basic VALUES (1, 'Priya', 9.20);
INSERT INTO Student_Basic VALUES (2, 'Arjun', 8.10);

COMMIT;


-- ── 2. ALTER TABLE SCHEMA MANIPULATION ─────────────────

-- Add new columns (Oracle doesn't require the KEYWORD 'COLUMN' for ADD)
ALTER TABLE Student_Basic ADD (phone VARCHAR2(15));
ALTER TABLE Student_Basic ADD (gender CHAR(1));

-- Modify column datatype and constraints
ALTER TABLE Student_Basic MODIFY (name VARCHAR2(100) NOT NULL);

-- Rename a column (Oracle syntax for changing column name)
ALTER TABLE Student_Basic RENAME COLUMN phone TO mobile;
ALTER TABLE Student_Basic MODIFY (mobile VARCHAR2(12));

-- Drop a column
ALTER TABLE Student_Basic DROP COLUMN gender;

-- Add check constraint validation
ALTER TABLE Student_Basic ADD CONSTRAINT chk_cgpa CHECK (cgpa BETWEEN 0 AND 10);

-- Describe table metadata schema structural definition
DESCRIBE Student_Basic;


-- ── 3. DATA TRUNCATION DEMO ────────────────────────────

CREATE TABLE TempStudent (
    id INT, 
    name VARCHAR2(30)
);

INSERT INTO TempStudent VALUES (1, 'Test');
COMMIT;

TRUNCATE TABLE TempStudent;

SELECT COUNT(*) AS rows_after_truncate FROM TempStudent;


-- ── 4. TABLE RENAMING AND DROP MANAGEMENT ──────────────

RENAME Student_Basic TO BEStudents;

-- View all active tables in current user schema (Replaces SHOW TABLES)
SELECT table_name FROM user_tables;

-- Drop table (Oracle doesn't support IF EXISTS natively, standard drop used)
DROP TABLE BEStudents;

-- Final verification of active schema tables
SELECT table_name FROM user_tables;


-- ── 5. ORACLE SYSTEM BACKUP UTILITY MANDATES ───────────
-- Run these commands from your Operating System Terminal/Command Prompt (Not inside SQL*Plus):
-- BACKUP:  expdp system/password@XE schemas=YOUR_SCHEMA directory=DATA_PUMP_DIR dumpfile=college_backup.dmp
-- RESTORE: impdp system/password@XE schemas=YOUR_SCHEMA directory=DATA_PUMP_DIR dumpfile=college_backup.dmp remap_schema=YOUR_SCHEMA:YOUR_SCHEMA


-------------------------
OUTPUT
-------------------------


1. Schema Description Output (DESCRIBE Student_Basic / BEStudents)

Name                                      Null?    Type
----------------------------------------- -------- ----------------------------
STUDENT_ID                                NOT NULL NUMBER(38)
NAME                                      NOT NULL VARCHAR2(100)
CGPA                                               NUMBER(4,2)
MOBILE                                             VARCHAR2(12)

2. Truncation Count Query Output

ROWS_AFTER_TRUNCATE
-------------------
                  0

3. First Table List Verification Output (After Rename)

TABLE_NAME
--------------------------------------------------------------------------------
DEPARTMENT
TEMPSTUDENT
BESTUDENTS

4. Final Table List Verification Output (After Drop)

TABLE_NAME
--------------------------------------------------------------------------------
DEPARTMENT
TEMPSTUDENT
