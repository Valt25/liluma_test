from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from bot.common.enums import CompanyOptions
from bot.db.connection import ConnectionCache

@dataclass(frozen=True, slots=True)
class CompanyData:
    months: List[str]
    data: List[str]

    def __post_init__(self):
        assert len(self.months) == len(self.data)


@dataclass(frozen=True, slots=True)
class Company:
    title: str
    sheet_id: str

async def get_companies() -> List[Company]:
    conn = ConnectionCache.get_connection()
    res = await conn.fetch(
        '''SELECT title, sheet_id FROM companies;'''
    )
    # stub logic, implement if have a time
    return [Company(i['title'], i['sheet_id']) for i in res]


async def get_company_data(company_name: str, company_option: CompanyOptions) -> CompanyData:
    conn = ConnectionCache.get_connection()
    res = await conn.fetch(f'''
        SELECT month, {company_option.value} FROM company_data JOIN companies ON company_data.company_id=companies.sheet_id WHERE title=$1
    ''', company_name)
    months = []
    data = []
    for r in res:
        months.append(r['month'])
        data.append(r[company_option.value])
    return CompanyData(months=months, data=data)

async def delete_companies_by_sheet_ids(sheet_ids: Set[str]):
    if len(sheet_ids) > 0:
        sheet_ids = [f"'{val}'" for val in sheet_ids]
        conn = ConnectionCache.get_connection()
        await conn.execute(f'''DELETE FROM companies WHERE sheet_id IN ({",".join(sheet_ids)})''')


async def update_companies(companies: List[Tuple[str, str]]):
    if len(companies) > 0:
        conn = ConnectionCache.get_connection()
        res = await conn.executemany(
            '''INSERT INTO companies (title, sheet_id) VALUES ($1, $2) ON CONFLICT(sheet_id) DO UPDATE SET title=EXCLUDED.title;''',
            companies
        )

async def update_data(companies_data: Dict[str, List[List[str]]]):
    conn = ConnectionCache.get_connection()
    data = []
    for sheet_id, company_data in companies_data.items():
        for item in company_data:
            item = [i.replace(',', '') for i in item]
            data.append((sheet_id, item[0].strip(), float(item[1]), float(item[2]), float(item[3]), float(item[4])))
    await conn.executemany(
        '''INSERT INTO company_data (company_id, month, income, expences, profit, KPN) VALUES ($1, $2, $3, $4, $5, $6) 
        ON CONFLICT(company_id, month) DO UPDATE SET income=EXCLUDED.income, expences=EXCLUDED.expences, profit=EXCLUDED.profit, KPN=EXCLUDED.KPN;''',
        data
    )