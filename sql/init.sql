CREATE DATABASE IF NOT EXISTS practice_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE practice_db;

-- ─────────────────────────────────────────────
-- TABLE 1: departments
-- ─────────────────────────────────────────────
CREATE TABLE departments (
    id       INT            AUTO_INCREMENT PRIMARY KEY,
    name     VARCHAR(100)   NOT NULL UNIQUE,
    location VARCHAR(100)   NOT NULL,
    budget   DECIMAL(15, 2) DEFAULT 0.00
);

INSERT INTO departments (name, location, budget) VALUES
  ('Engineering', 'Kyiv',     1500000.00),
  ('Marketing',   'Lviv',      800000.00),
  ('HR',          'Kyiv',      400000.00),
  ('Sales',       'Odesa',    1200000.00),
  ('QA',          'Kharkiv',   600000.00);

-- ─────────────────────────────────────────────
-- TABLE 2: employees
-- ─────────────────────────────────────────────
CREATE TABLE employees (
    id            INT            AUTO_INCREMENT PRIMARY KEY,
    first_name    VARCHAR(50)    NOT NULL,
    last_name     VARCHAR(50)    NOT NULL,
    email         VARCHAR(100)   NOT NULL UNIQUE,
    job_title     VARCHAR(100)   NOT NULL,
    salary        DECIMAL(10, 2) NOT NULL,
    hire_date     DATE           NOT NULL,
    is_active     BOOLEAN        DEFAULT TRUE,
    department_id INT,
    CONSTRAINT fk_emp_dept FOREIGN KEY (department_id)
        REFERENCES departments (id) ON DELETE SET NULL
);

INSERT INTO employees (first_name, last_name, email, job_title, salary, hire_date, is_active, department_id) VALUES
  ('Olena',   'Kovalenko',    'o.kovalenko@company.com',   'Backend Developer',     95000.00, '2020-03-15', TRUE,  1),
  ('Dmytro',  'Bondarenko',   'd.bondarenko@company.com',  'Frontend Developer',    87000.00, '2021-06-01', TRUE,  1),
  ('Iryna',   'Savchenko',    'i.savchenko@company.com',   'DevOps Engineer',      105000.00, '2019-11-20', TRUE,  1),
  ('Mykola',  'Tkachenko',    'm.tkachenko@company.com',   'QA Engineer',           72000.00, '2022-01-10', TRUE,  5),
  ('Natalia', 'Moroz',        'n.moroz@company.com',       'QA Lead',               98000.00, '2020-07-18', TRUE,  5),
  ('Serhiy',  'Kravchenko',   's.kravchenko@company.com',  'Marketing Manager',     88000.00, '2018-04-05', TRUE,  2),
  ('Oksana',  'Petrenko',     'o.petrenko@company.com',    'Content Specialist',    61000.00, '2023-02-28', TRUE,  2),
  ('Vasyl',   'Lysenko',      'v.lysenko@company.com',     'HR Manager',            75000.00, '2017-09-12', TRUE,  3),
  ('Yulia',   'Shevchenko',   'y.shevchenko@company.com',  'HR Specialist',         55000.00, '2023-08-01', TRUE,  3),
  ('Andriy',  'Kovalchuk',    'a.kovalchuk@company.com',   'Sales Manager',         92000.00, '2019-05-22', TRUE,  4),
  ('Tetiana', 'Hrytsenko',    't.hrytsenko@company.com',   'Sales Specialist',      67000.00, '2021-11-15', TRUE,  4),
  ('Roman',   'Sydorenko',    'r.sydorenko@company.com',   'Senior Developer',     115000.00, '2016-03-30', FALSE, 1),
  ('Larysa',  'Marchenko',    'l.marchenko@company.com',   'Data Analyst',          83000.00, '2022-06-14', TRUE,  1),
  ('Pavlo',   'Zakharchenko', 'p.zakharchenko@company.com','Sales Specialist',      71000.00, '2020-12-01', TRUE,  4),
  ('Halyna',  'Bilous',       'h.bilous@company.com',      'Marketing Specialist',  58000.00, '2024-01-09', TRUE,  2);

-- ─────────────────────────────────────────────
-- TABLE 3: projects
-- ─────────────────────────────────────────────
CREATE TABLE projects (
    id               INT            AUTO_INCREMENT PRIMARY KEY,
    name             VARCHAR(150)   NOT NULL,
    description      TEXT,
    status           ENUM('planned','active','completed','cancelled') DEFAULT 'planned',
    budget           DECIMAL(12, 2) NOT NULL,
    start_date       DATE,
    end_date         DATE,
    department_id    INT,
    lead_employee_id INT,
    CONSTRAINT fk_proj_dept FOREIGN KEY (department_id)
        REFERENCES departments (id) ON DELETE SET NULL,
    CONSTRAINT fk_proj_lead FOREIGN KEY (lead_employee_id)
        REFERENCES employees (id) ON DELETE SET NULL
);

INSERT INTO projects (name, description, status, budget, start_date, end_date, department_id, lead_employee_id) VALUES
  ('Platform Rewrite',       'Full backend rewrite to microservices', 'active',    320000.00, '2024-01-01', '2024-12-31', 1,  3),
  ('Mobile App v2',          'New mobile application release',        'active',    180000.00, '2024-03-01', '2024-09-30', 1,  1),
  ('E2E Test Automation',    'Automate regression test suite',        'completed',  75000.00, '2023-06-01', '2023-12-31', 5,  5),
  ('Performance Testing',    'Load & stress testing initiative',      'active',     45000.00, '2024-04-01', '2024-07-31', 5,  4),
  ('Brand Campaign Q3',      'Summer brand awareness campaign',       'completed',  95000.00, '2023-07-01', '2023-09-30', 2,  6),
  ('SEO Optimization',       'Improve organic search ranking',        'active',     30000.00, '2024-02-15', NULL,         2,  7),
  ('Talent Acquisition',     'Hire 20 engineers by Q4',               'active',     50000.00, '2024-01-10', '2024-12-31', 3,  8),
  ('CRM Implementation',     'Deploy new CRM for sales team',         'planned',   140000.00, '2024-08-01', '2025-02-28', 4, 10),
  ('Sales Training Program', 'Quarterly sales skills training',       'completed',  20000.00, '2023-10-01', '2023-10-31', 4, 11),
  ('Data Warehouse',         'Centralized analytics data warehouse',  'planned',   250000.00, '2024-10-01', '2025-06-30', 1, 13),
  ('API Gateway',            'Unified API gateway for all services',  'cancelled',  60000.00, '2023-01-01', '2023-06-30', 1,  1);

