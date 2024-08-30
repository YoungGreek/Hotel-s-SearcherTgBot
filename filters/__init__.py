from loader import dp
from .limit_filter import LimitFilter
from .date_filter import DateFilter

if __name__ == 'filters':
    dp.filters_factory.bind(LimitFilter)
    dp.filters_factory.bind(DateFilter)
