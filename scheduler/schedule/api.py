import requests, datetime
from xml.etree import ElementTree

from django.conf import settings

from .models import Holiday


class HolidayAPI(object):
    def __init__(self):
        self.holiday_base_url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/{holiday_kinds}?"\
                                "solYear={year}&solMonth={month}&ServiceKey=%s" % settings.API_KEY
        self.parse_category = ("getHoliDeInfo", "getRestDeInfo", "get24DivisionsInfo", "getSundryDayInfo",)

    def __call__(self, *args, **kwargs):
        for category in self.parse_category:
            self.api_parser(category)

    def api_parser(self, holiday_kinds):
        for year in range(2015, 2021):
            year = str(year)
            for month in range(1, 13):
                month = str(month).zfill(2)

                response = requests.get(
                    self.holiday_base_url.format(
                        holiday_kinds=holiday_kinds,
                        year=year,
                        month=month
                    )
                )
                root = ElementTree.fromstring(response.text)
                items = root.iter('item')

                for item in items:
                    name = item.find('dateName').text
                    is_holiday = item.find('isHoliday').text
                    date = item.find('locdate').text

                    is_holiday = True if is_holiday == 'Y' else False

                    date = datetime.datetime.strptime(date, "%Y%m%d")
                    self.save_holiday(name, is_holiday, date)

    @staticmethod
    def save_holiday(name, is_holiday, date):
        Holiday.objects.get_or_create(name=name, is_holiday=is_holiday, date=date)


h = HolidayAPI()()
