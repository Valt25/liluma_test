from bot.common.enums import CompanyOptions


MESSAGE_WITH_COMPANY_LIST_TEXT = "Выберете компанию для просмотра статистики:"
COMPANY_OPTION_ENUM_TO_TEXT = {
    CompanyOptions.INCOME: 'Доход компании',
    CompanyOptions.EXPENCES: 'Расход компании',
    CompanyOptions.PROFIT: 'Прибыль компании',
    CompanyOptions.KPN: 'КПН компании',
}
MESSAGE_WITH_COMPANY_OPTIONS_TEXT = "Выберете для данной компании тип информации:"
BACK_BUTTON_TEXT = 'Назад'
COMPANY_DATA_PRESENTATION_TEXT = "Посмотрите на данные(они вам нравятся?):"