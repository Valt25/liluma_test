import io
import matplotlib.pyplot as plt

from bot.services.companies import CompanyData
from bot.common.enums import CompanyOptions
from bot import texts

async def get_plot(company_data: CompanyData, company_name: str = None, company_option: CompanyOptions = None) -> io.BytesIO:
    _, ax = plt.subplots()
    ax.bar(company_data.months, company_data.data, label=company_data.months)
    if company_name is not None or company_option is not None:
        ax.set_title(f'{company_name if company_name is not None else 'None company'} data with option {texts.COMPANY_OPTION_ENUM_TO_TEXT[company_option] if company_option is not None else ''}')
    buff = io.BytesIO()
    plt.savefig(buff, format='png')
    buff.seek(0)
    return buff