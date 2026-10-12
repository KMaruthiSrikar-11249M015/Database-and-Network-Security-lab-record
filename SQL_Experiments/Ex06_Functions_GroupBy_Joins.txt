EXP-6

-- ── 1. TABLE CREATION ──────────────────────────────────

CREATE TABLE dept (
    dept_id INT PRIMARY KEY, 
    dept_name VARCHAR2(30), 
    hod VARCHAR2(30)
);

CREATE TABLE emp (
    emp_id INT PRIMARY KEY, 
    emp_name VARCHAR2(40), 
    dept_id INT, 
    salary NUMBER(10,2), 
    join_date DATE, 
    city VARCHAR2(20),
    FOREIGN KEY (dept_id) REFERENCES dept(dept_id)
);


-- ── 2. DATA INSERTION ──────────────────────────────────

INSERT INTO dept VALUES (1, 'CSE', 'Dr. Sharma');
INSERT INTO dept VALUES (2, 'ECE', 'Dr. Patel');
INSERT INTO dept VALUES (3, 'MECH', 'Dr. Kumar');

INSERT INTO emp VALUES (1, 'Priya', 1, 55000, TO_DATE('2020-06-15', 'YYYY-MM-DD'), 'Chennai');
INSERT INTO emp VALUES (2, 'Arjun', 1, 62000, TO_DATE('2019-03-10', 'YYYY-MM-DD'), 'Bangalore');
INSERT INTO emp VALUES (3, 'Kavya', 2, 48000, TO_DATE('2021-08-22', 'YYYY-MM-DD'), 'Chennai');
INSERT INTO emp VALUES (4, 'Ravi', 2, 71000, TO_DATE('2018-11-05', 'YYYY-MM-DD'), 'Delhi');
INSERT INTO emp VALUES (5, 'Deepika', 3, 43000, TO_DATE('2022-01-30', 'YYYY-MM-DD'), 'Chennai');
INSERT INTO emp VALUES (6, 'Siva', 3, 38000, TO_DATE('2020-09-18', 'YYYY-MM-DD'), 'Mumbai');

COMMIT;


-- ── 3. DATA VERIFICATION & BUILT-IN FUNCTIONS ─────────

-- SQL*Plus Formatting commands for clean output terminal layout
SET PAGESIZE 100;
SET LINESIZE 150;
COLUMN emp_name FORMAT A10;
COLUMN city FORMAT A10;
COLUMN dept_name FORMAT A10;
COLUMN hod FORMAT A12;
COLUMN formatted_date FORMAT A12;
COLUMN full_desc FORMAT A22;

-- Basic Filter Queries
SELECT * FROM emp;
SELECT emp_name, salary FROM emp WHERE city='Chennai';
SELECT emp_name, salary FROM emp WHERE salary BETWEEN 40000 AND 60000;
SELECT emp_name, salary FROM emp ORDER BY salary DESC;
SELECT DISTINCT city FROM emp;
SELECT emp_name FROM emp WHERE emp_name LIKE 'A%';

-- Row Limiting (Replaces MySQL LIMIT 3)
SELECT * FROM emp FETCH FIRST 3 ROWS ONLY;

-- Group Aggregate Scalar Evaluators
SELECT COUNT(*) AS total_employees FROM emp;
SELECT SUM(salary) AS total_payroll FROM emp;
SELECT ROUND(AVG(salary),2) AS avg_salary FROM emp;
SELECT MAX(salary) AS highest_salary FROM emp;
SELECT MIN(salary) AS lowest_salary FROM emp;

-- Grouping blocks & Having Conditionals
SELECT dept_id, COUNT(*) AS headcount, ROUND(AVG(salary),2) AS avg_salary, SUM(salary) AS total_salary FROM emp GROUP BY dept_id;
SELECT dept_id, ROUND(AVG(salary),2) AS avg_sal FROM emp GROUP BY dept_id HAVING AVG(salary)>50000;
SELECT city, COUNT(*) AS cnt FROM emp GROUP BY city HAVING COUNT(*)>=2 ORDER BY cnt DESC;

-- Date & Time System Operations (Oracle Variants)
SELECT CURRENT_TIMESTAMP, SYSDATE FROM dual;

SELECT emp_name, join_date, 
       EXTRACT(YEAR FROM join_date) AS join_year, 
       EXTRACT(MONTH FROM join_date) AS join_month, 
       EXTRACT(DAY FROM join_date) AS join_day,
       TO_CHAR(join_date, 'DAY') AS day_name 
FROM emp;

SELECT emp_name, ROUND(MONTHS_BETWEEN(SYSDATE, join_date)/12, 1) AS years_exp FROM emp;
SELECT emp_name, join_date + INTERVAL '1' YEAR AS anniversary FROM emp;
SELECT emp_name, TO_CHAR(join_date, 'DD-MON-YYYY') AS formatted_date FROM emp;

-- String Functional Operations
SELECT emp_name, 
       UPPER(emp_name) AS up_name, 
       LOWER(emp_name) AS low_name, 
       LENGTH(emp_name) AS len_name, 
       SUBSTR(emp_name, 1, 3) AS sub_str, 
       emp_name || ' - ' || city AS full_desc, 
       REPLACE(city, 'Chennai', 'Madras') AS rep_city
FROM emp;

-- Numerical & Mathematical Calculations via Dual View
SELECT ROUND(3.14159,2) AS r_val, CEIL(4.1) AS c_val, FLOOR(4.9) AS f_val, ABS(-250) AS a_val, MOD(10,3) AS m_val, POWER(2,8) AS p_val, SQRT(144) AS s_val, TRUNC(3.99999,2) AS t_val FROM dual;


-- ── 4. ADVANCED DATABASE JOIN CLAUSES ─────────────────

SELECT e.emp_name, e.salary, d.dept_name, d.hod FROM emp e INNER JOIN dept d ON e.dept_id=d.dept_id;
SELECT e.emp_name, d.dept_name FROM emp e LEFT JOIN dept d ON e.dept_id=d.dept_id;
SELECT e.emp_name, d.dept_name FROM emp e RIGHT JOIN dept d ON e.dept_id=d.dept_id;
SELECT e.emp_name, d.dept_name FROM emp e CROSS JOIN dept d;

-- Self Join Execution Block
SELECT a.emp_name AS emp, b.emp_name AS colleague FROM emp a JOIN emp b ON a.dept_id=b.dept_id AND a.emp_id<>b.emp_id;

-- Complex Aggregate Grouping Joins View
SELECT d.dept_name, COUNT(e.emp_id) AS headcount, ROUND(AVG(e.salary),2) AS avg_sal FROM dept d LEFT JOIN emp e ON d.dept_id=e.dept_id GROUP BY d.dept_name ORDER BY avg_sal DESC;




-----------------------
OUTPUT
-----------------------

Scalar Aggregates View

TOTAL_EMPLOYEES
---------------
              6

TOTAL_PAYROLL
-------------
       317000

AVG_SALARY
----------
  52833.33

HIGHEST_SALARY
--------------
         71000

LOWEST_SALARY
-------------
        38000

Group By Headcount Summaries View

   DEPT_ID  HEADCOUNT AVG_SALARY TOTAL_SALARY
---------- ---------- ---------- ------------
         1          2      58500       117000
         2          2      59500       119000
         3          2      40500        81000

Having Constraint Filters Output

   DEPT_ID    AVG_SAL_
---------- -----------
         1       58500
         2       59500

Math Calculation Result View

     R_VAL      C_VAL      F_VAL      A_VAL      M_VAL      P_VAL      S_VAL      T_VAL
---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------
      3.14          5          4        250          1        256         12       3.99

Department Join Aggregate Output

DEPT_NAME   HEADCOUNT    AVG_SAL
---------- ---------- ----------
ECE                 2      59500
CSE                 2      58500
MECH                2      40500
