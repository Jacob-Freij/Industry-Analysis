SELECT COUNT(*) FROM job_vacancies;

SELECT naics_sector, COUNT(*)
FROM job_vacancies
GROUP BY naics_sector
ORDER BY naics_sector;

SELECT TOP (15) *
FROM job_vacancies
WHERE naics_sector = 'Utilities'
ORDER BY ref_date;

SELECT TOP (1) ref_date, job_vacancy_rate
FROM job_vacancies
WHERE naics_sector = 'Professional, scientific and technical services'
ORDER BY job_vacancy_rate DESC;

SELECT TOP (1) ref_date, job_vacancy_rate
FROM job_vacancies
WHERE naics_sector = 'Total, all industries'
ORDER BY job_vacancy_rate DESC;

SELECT
    t.ref_date,
    t.job_vacancy_rate AS baseline_rate,
    p.job_vacancy_rate AS psts_rate,
    ROUND(p.job_vacancy_rate - t.job_vacancy_rate, 2) AS spread
FROM job_vacancies t
JOIN job_vacancies p ON t.ref_date = p.ref_date
WHERE t.naics_sector = 'Total, all industries'
  AND p.naics_sector = 'Professional, scientific and technical services'
ORDER BY t.ref_date;

SELECT
    ROUND(AVG(p.job_vacancy_rate - t.job_vacancy_rate), 2) AS avg_spread,
    ROUND(MIN(p.job_vacancy_rate - t.job_vacancy_rate), 2) AS min_spread,
    ROUND(MAX(p.job_vacancy_rate - t.job_vacancy_rate), 2) AS max_spread
FROM job_vacancies t
JOIN job_vacancies p ON t.ref_date = p.ref_date
WHERE t.naics_sector = 'Total, all industries'
  AND p.naics_sector = 'Professional, scientific and technical services';

SELECT t.ref_date, ROUND(p.job_vacancy_rate - t.job_vacancy_rate, 2) AS spread
FROM job_vacancies t
JOIN job_vacancies p ON t.ref_date = p.ref_date
WHERE t.naics_sector = 'Total, all industries'
  AND p.naics_sector = 'Professional, scientific and technical services'
  AND t.ref_date >= '2022-01-01' AND t.ref_date <= '2023-01-01'
ORDER BY t.ref_date;


SELECT
    ref_date,
    MAX(CASE WHEN naics_sector = 'Total, all industries' THEN job_vacancy_rate END) AS baseline,
    MAX(CASE WHEN naics_sector = 'Arts, entertainment and recreation' THEN job_vacancy_rate END) AS arts_rate,
    MAX(CASE WHEN naics_sector = 'Arts, entertainment and recreation' THEN payroll_employees END) AS arts_employees,
    MAX(CASE WHEN naics_sector = 'Retail trade' THEN job_vacancy_rate END) AS retail_rate,
    MAX(CASE WHEN naics_sector = 'Retail trade' THEN payroll_employees END) AS retail_employees
FROM job_vacancies
WHERE ref_date >= '2019-06-01' AND ref_date <= '2022-06-01'
GROUP BY ref_date
ORDER BY ref_date;

SELECT
    'Arts, entertainment and recreation' AS sector,
    ROUND(AVG(s.job_vacancy_rate - t.job_vacancy_rate), 2) AS avg_spread_full,
    ROUND(MIN(s.job_vacancy_rate - t.job_vacancy_rate), 2) AS min_spread_full,
    ROUND(MAX(s.job_vacancy_rate - t.job_vacancy_rate), 2) AS max_spread_full,
    ROUND(AVG(CASE WHEN t.ref_date BETWEEN '2020-01-01' AND '2021-12-01'
        THEN s.job_vacancy_rate - t.job_vacancy_rate END), 2) AS avg_spread_pandemic
FROM job_vacancies t
JOIN job_vacancies s ON t.ref_date = s.ref_date
WHERE t.naics_sector = 'Total, all industries'
  AND s.naics_sector = 'Arts, entertainment and recreation'

UNION ALL

SELECT
    'Retail trade',
    ROUND(AVG(s.job_vacancy_rate - t.job_vacancy_rate), 2),
    ROUND(MIN(s.job_vacancy_rate - t.job_vacancy_rate), 2),
    ROUND(MAX(s.job_vacancy_rate - t.job_vacancy_rate), 2),
    ROUND(AVG(CASE WHEN t.ref_date BETWEEN '2020-01-01' AND '2021-12-01'
        THEN s.job_vacancy_rate - t.job_vacancy_rate END), 2)
FROM job_vacancies t
JOIN job_vacancies s ON t.ref_date = s.ref_date
WHERE t.naics_sector = 'Total, all industries'
  AND s.naics_sector = 'Retail trade';



SELECT
    naics_sector,
    ROUND(AVG(CASE WHEN ref_date BETWEEN '2019-01-01' AND '2019-12-01'
        THEN payroll_employees END), 0) AS avg_employees_2019,
    ROUND(AVG(CASE WHEN ref_date BETWEEN '2020-04-01' AND '2020-12-01'
        THEN payroll_employees END), 0) AS avg_employees_pandemic_low,
    ROUND(
        AVG(CASE WHEN ref_date BETWEEN '2020-04-01' AND '2020-12-01' THEN payroll_employees END)
        - AVG(CASE WHEN ref_date BETWEEN '2019-01-01' AND '2019-12-01' THEN payroll_employees END)
    , 0) AS employee_change
FROM job_vacancies
WHERE naics_sector IN ('Arts, entertainment and recreation', 'Retail trade')
GROUP BY naics_sector;

SELECT ref_date, job_vacancies, payroll_employees, job_vacancy_rate
FROM job_vacancies
WHERE naics_sector = 'Arts, entertainment and recreation'
  AND ref_date BETWEEN '2019-06-01' AND '2021-12-01'
ORDER BY ref_date;