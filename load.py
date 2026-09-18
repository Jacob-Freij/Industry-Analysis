import pandas as pd
import sqlite3

# --- Step 1: Read the raw CSV ---
# This loads the whole CSV into a DataFrame — think of it as an
# in-memory spreadsheet you can filter/reshape with code instead of clicking.
df = pd.read_csv('Data/raw_job_vacancies.csv')
print(df['REF_DATE'].head(10).tolist())
# --- Step 2: Split the NAICS column into code + clean sector name ---
# "Professional, scientific and technical services [54]" becomes:
#   naics_sector = "Professional, scientific and technical services"
#   naics_code   = "54"
naics_col = 'North American Industry Classification System (NAICS)'
df['naics_code'] = df[naics_col].str.extract(r'\[([\d\-]+)\]')
df['naics_sector'] = df[naics_col].str.replace(r'\s*\[[\d\-]+\]', '', regex=True)

# --- Step 3: Parse the date properly ---
df['ref_date'] = pd.to_datetime(df['REF_DATE'], format='%y-%b')

# --- Step 4: Pivot ---
# Right now you have 3 rows per sector-month (one per Statistics value).
# .pivot() reshapes that into 1 row per sector-month, with separate
# columns for each Statistics value's VALUE and STATUS.
pivoted = df.pivot(
    index=['ref_date', 'naics_sector', 'naics_code'],
    columns='Statistics',
    values=['VALUE', 'STATUS']
)

# pivot() gives you two-level column names like ('VALUE', 'Job vacancies').
# Flatten those into single names you'll actually want to type in SQL.
pivoted.columns = ['_'.join(col).strip() for col in pivoted.columns]
pivoted = pivoted.reset_index()

pivoted = pivoted.rename(columns={
    'VALUE_Job vacancies': 'job_vacancies',
    'VALUE_Payroll employees': 'payroll_employees',
    'VALUE_Job vacancy rate': 'job_vacancy_rate',
    'STATUS_Job vacancies': 'vacancies_status',
    'STATUS_Payroll employees': 'employees_status',
    'STATUS_Job vacancy rate': 'rate_status',
})

# --- Step 5: Sanity check before writing ---
print(pivoted.shape)
print(pivoted.head())
print(pivoted['ref_date'].min(), pivoted['ref_date'].max())

# --- Step 6: Write to SQLite ---
# sqlite3.connect() creates job_vacancies.db if it doesn't exist yet.
conn = sqlite3.connect('job_vacancies.db')
pivoted.to_sql('job_vacancies', conn, if_exists='replace', index=False)
conn.close()

print("Done.")