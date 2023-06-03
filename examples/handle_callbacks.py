"""
In order to correctly process callbacks about the buttons pressed on the calendar, you need to do the following:
"""
import datetime

from telebot import TeleBot, types

from calendar_pytba.utils.types import CalendarLanguage, CallBackData

bot = TeleBot("SOME_TOKEN")

# 1. In the file where you handle the callbacks (where you call the bot.process_new_updates([updates])
# method on the TeleBot class instance), import the handler:

from calendar_pytba.utils.handler import callback_handler

# 2. Call the function with your parameters

callback_handler(bot, CalendarLanguage.EN)

# 3. Done. Now all button clicks will be processed by your bot automatically

# The only thing left for you to do is to correctly handle the click of the button with the selected date.
# Example below:


@bot.callback_query_handler(
    func=lambda call: call.data.startswith(CallBackData.SELECTED_DATE)
)
def selected_date_callback(call: types.CallbackQuery) -> None:
    date_as_string = call.data.split(":")[1]
    date = datetime.datetime.strptime(date_as_string, "%Y-%m-%d")
    # Do whatever you want with the date
    answer_text = f"Your date is {date.strftime('%d.%m.%Y')}"
    bot.send_message(call.message.chat.id, answer_text)


# P.S. You can always redefine callback handlers yourself. Look at the examples from calendar_pytba.utils.handler.py
