# This is an example of how the library works

import datetime

from telebot import TeleBot, types

from calendar_pytba import Calendar
from calendar_pytba.utils.types import CalendarLanguage

bot = TeleBot("SOME_TOKEN")


@bot.message_handler(commands=["calendar"])
def calendar_command(message: types.Message) -> None:
    """
    This is an example of creating a calendar buttons. By initializing an instance of the class,
    you can pass in the language in which the names of the months and days of the week
    will be written. The value can be passed as a string ("en", for example), or you can refer to the
    attributes of the CalendarLanguage class

    By default, the get_calendar() method will return a calendar with the current date. But you can
    also pass your date from which you want to display the calendar
    """

    start_date = datetime.date(2020, 1, 1)
    calendar = Calendar(CalendarLanguage.EN)
    markup = calendar.get_calendar(start_date)
    bot.send_message(message.chat.id, "Select date", reply_markup=markup)
