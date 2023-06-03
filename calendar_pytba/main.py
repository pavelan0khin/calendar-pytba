import calendar
import datetime

from dateutil.relativedelta import relativedelta
from telebot import types  # noqa

from calendar_pytba.utils import text
from calendar_pytba.utils.types import CalendarLanguage, CallBackData


class Calendar:
    def __init__(
        self,
        language: str = CalendarLanguage.EN,
        empty_day_symbol: str = " ",
        next_page_symbol: str = "→",
        previous_page_symbol: str = "←",
        month_names: dict = text.MONTH_NAMES,
        week_days_names: dict = text.WEEK_DAYS_NAMES,
        week_days_short_names: dict = text.WEEK_DAYS_SHORT_NAMES,
    ):
        """
        The language is responsible for writing the names of the months,
        days of the week, and other elements of the calendar.
        You can pass the language value as a string, see available
        languages in calendar_pytba.utils.types.CalendarLanguage
        :param language: str, CalendarLanguage class attribute
        :param empty_day_symbol: str, character to be displayed on days of the week where there are no numbers
        :param next_page_symbol: str, scroll forward button symbol
        :param previous_page_symbol: str, scroll backward button symbol
        :param month_names: dict, dictionary with the names of the months
        :param week_days_names: dict, dictionary with the names of the weekdays
        :param week_days_short_names: dict, dictionary with the short names of the weekdays
        """
        self.language = language
        self.markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(
            row_width=7
        )
        self.empty_day_symbol = empty_day_symbol
        self.next_page_symbol = next_page_symbol
        self.previous_page_symbol = previous_page_symbol
        self.month_names = month_names
        self.week_days_names = week_days_names
        self.week_days_short_names = week_days_short_names

    def _get_month_name(self, month: int) -> str:
        return self.month_names.get(self.language).get(month)

    def _add_headline(self, date: datetime.date):
        self.markup.add(
            types.InlineKeyboardButton(
                self._get_month_name(date.month),
                callback_data=f"{CallBackData.LIST_MONTHS}:{date.year}",
            ),
            types.InlineKeyboardButton(
                date.year,
                callback_data=f"{CallBackData.LIST_YEARS}:{date.month}:{date.year}",
            ),
        )

    def _add_weekdays_line(self):
        weekdays = self.week_days_short_names.get(self.language)
        buttons = [
            types.InlineKeyboardButton(
                weekdays.get(weekday),
                callback_data=f"{CallBackData.FULL_WEEKDAY_NAME}:{weekday}",
            )
            for weekday in weekdays
        ]
        self.markup.add(*buttons)

    def _add_weeks(self, date: datetime.date):
        start_week_day, days_in_month = calendar.monthrange(date.year, date.month)
        week = []
        empty_day = types.InlineKeyboardButton(
            self.empty_day_symbol, callback_data=CallBackData.EMPTY_WEEKDAY
        )
        for _ in range(start_week_day):
            week.append(empty_day)
        for day in range(days_in_month):
            if len(week) == 7:
                self.markup.add(*week)
                week = []
            month_day = day + 1
            date_for_callback = (
                f"{date.year}-{str(date.month).zfill(2)}-{str(month_day).zfill(2)}"
            )
            week.append(
                types.InlineKeyboardButton(
                    str(month_day),
                    callback_data=f"{CallBackData.SELECTED_DATE}:{date_for_callback}",
                )
            )
        for _ in range(7 - len(week)):
            week.append(empty_day)
        self.markup.add(*week)

    def _add_last_line(self, date: datetime.date):
        next_month_date = date + relativedelta(months=1)
        previous_month_date = date - relativedelta(months=1)
        self.markup.add(
            types.InlineKeyboardButton(
                self.previous_page_symbol,
                callback_data=f"{CallBackData.FLIP_CALENDAR}:{previous_month_date.month}:{previous_month_date.year}",
            ),
            types.InlineKeyboardButton(
                self.next_page_symbol,
                callback_data=f"{CallBackData.FLIP_CALENDAR}:{next_month_date.month}:{next_month_date.year}",
            ),
        )

    def get_calendar(
        self, displayed_date: datetime.date = datetime.datetime.now().date()
    ) -> types.InlineKeyboardMarkup:
        """
        Creates an InlineKeyboardMarkup calendar based on the date in the method arguments.
        By default, a calendar is created for the current month

        :param displayed_date: Date to display on the calendar
        """
        self.markup = types.InlineKeyboardMarkup(row_width=7)
        self._add_headline(displayed_date)
        self._add_weekdays_line()
        self._add_weeks(displayed_date)
        self._add_last_line(displayed_date)
        return self.markup

    def get_list_months(self, year: int) -> types.InlineKeyboardMarkup:
        """
        Getting a list of months as InlineKeyboardMarkup
        :param year: the parameter is required so that after selecting the month, the year that
               was specified is displayed
        """
        self.markup = types.InlineKeyboardMarkup(row_width=3)
        month_names: dict = self.month_names.get(self.language)
        buttons = []
        for month, month_name in month_names.items():
            buttons.append(
                types.InlineKeyboardButton(
                    month_name,
                    callback_data=f"{CallBackData.SELECTED_MONTH}:{month}:{year}",
                )
            )
        self.markup.add(*buttons)
        return self.markup

    def get_list_years(self, month: int, year: int) -> types.InlineKeyboardMarkup:
        """
        Getting a list of years as InlineKeyboardMarkup
        :param month: The month to display after the user selects a year
        :param year: The year to be displayed in the list of years in the middle
        """
        self.markup = types.InlineKeyboardMarkup(row_width=3)
        start_year = year - 4
        buttons = []
        for _ in range(9):
            buttons.append(
                types.InlineKeyboardButton(
                    str(start_year),
                    callback_data=f"{CallBackData.SELECTED_YEAR}:{month}:{start_year}",
                )
            )
            start_year += 1
        self.markup.add(*buttons)
        self.markup.add(
            types.InlineKeyboardButton(
                self.previous_page_symbol,
                callback_data=f"{CallBackData.PREVIOUS_YEARS}:{month}:{year}",
            ),
            types.InlineKeyboardButton(
                self.next_page_symbol,
                callback_data=f"{CallBackData.NEXT_YEARS}:{month}:{year}",
            ),
        )
        return self.markup
