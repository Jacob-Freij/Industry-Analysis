import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
conn = sqlite3.connect(BASE_DIR / 'job_vacancies.db')
figures_dir = BASE_DIR / 'figures'
figures_dir.mkdir(exist_ok=True)

# ---------------------------------------------------------------
# Chart 1 — PSTS vs. All Industries, with spread shaded
# ---------------------------------------------------------------
query_psts = """
SELECT
    t.ref_date,
    t.job_vacancy_rate AS baseline,
    p.job_vacancy_rate AS psts
FROM job_vacancies t
JOIN job_vacancies p ON t.ref_date = p.ref_date
WHERE t.naics_sector = 'Total, all industries'
  AND p.naics_sector = 'Professional, scientific and technical services'
ORDER BY t.ref_date;
"""
df_psts = pd.read_sql(query_psts, conn, parse_dates=['ref_date'])

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(df_psts['ref_date'], df_psts['baseline'], label='All industries', linewidth=2, color='#555555')
ax.plot(df_psts['ref_date'], df_psts['psts'], label='Professional, scientific & technical services', linewidth=2, color='#2166ac')
ax.fill_between(df_psts['ref_date'], df_psts['baseline'], df_psts['psts'],
                 where=(df_psts['psts'] >= df_psts['baseline']), alpha=0.15, color='#2166ac')
ax.fill_between(df_psts['ref_date'], df_psts['baseline'], df_psts['psts'],
                 where=(df_psts['psts'] < df_psts['baseline']), alpha=0.15, color='#b2182b')

ax.set_title('Job Vacancy Rate: PSTS vs. All Industries (2015–2026)')
ax.set_ylabel('Job vacancy rate (%)')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(figures_dir / 'psts_vs_baseline.png', dpi=150)
plt.close(fig)

# ---------------------------------------------------------------
# Chart 2 — Retail Trade vs. All Industries
# ---------------------------------------------------------------
query_retail = """
SELECT
    t.ref_date,
    t.job_vacancy_rate AS baseline,
    r.job_vacancy_rate AS retail
FROM job_vacancies t
JOIN job_vacancies r ON t.ref_date = r.ref_date
WHERE t.naics_sector = 'Total, all industries'
  AND r.naics_sector = 'Retail trade'
ORDER BY t.ref_date;
"""
df_retail = pd.read_sql(query_retail, conn, parse_dates=['ref_date'])

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(df_retail['ref_date'], df_retail['baseline'], label='All industries', linewidth=2, color='#555555')
ax.plot(df_retail['ref_date'], df_retail['retail'], label='Retail trade', linewidth=2, color='#4daf4a')

ax.set_title('Job Vacancy Rate: Retail Trade vs. All Industries (2015–2026)')
ax.set_ylabel('Job vacancy rate (%)')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(figures_dir / 'retail_vs_baseline.png', dpi=150)
plt.close(fig)

# ---------------------------------------------------------------
# Chart 3 — Arts, Entertainment & Recreation: payroll vs. vacancies (dual axis)
# ---------------------------------------------------------------
query_arts = """
SELECT ref_date, job_vacancies, payroll_employees
FROM job_vacancies
WHERE naics_sector = 'Arts, entertainment and recreation'
ORDER BY ref_date;
"""
df_arts = pd.read_sql(query_arts, conn, parse_dates=['ref_date'])

fig, ax1 = plt.subplots(figsize=(11, 5))

ax1.plot(df_arts['ref_date'], df_arts['payroll_employees'], color='#555555', linewidth=2, label='Payroll employees')
ax1.set_ylabel('Payroll employees', color='#555555')
ax1.tick_params(axis='y', labelcolor='#555555')

ax2 = ax1.twinx()
ax2.plot(df_arts['ref_date'], df_arts['job_vacancies'], color='#e6550d', linewidth=2, label='Job vacancies')
ax2.set_ylabel('Job vacancies', color='#e6550d')
ax2.tick_params(axis='y', labelcolor='#e6550d')

ax1.set_title('Arts, Entertainment & Recreation: Payroll Collapse vs. Vacancy Spike (2015–2026)')
ax1.grid(alpha=0.3)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()
plt.savefig(figures_dir / 'arts_payroll_vs_vacancies.png', dpi=150)
plt.close(fig)

conn.close()
print("All three charts saved to:", figures_dir)