from telebot import types

button_search_nearby = types.InlineKeyboardButton(text="/search_nearby")
button_search_by_name = types.InlineKeyboardButton(text="/search_by_name")
button_settings = types.InlineKeyboardButton(text="/settings")
button_set_radius = types.InlineKeyboardButton(text="/set_radius")
button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
button_help = types.InlineKeyboardButton(text="/help")


button_1 = types.InlineKeyboardButton(text="1")
button_2 = types.InlineKeyboardButton(text="2")
button_3 = types.InlineKeyboardButton(text="3")
button_4 = types.InlineKeyboardButton(text="4")
button_5 = types.InlineKeyboardButton(text="5")
button_6 = types.InlineKeyboardButton(text="6")
button_7 = types.InlineKeyboardButton(text="7")
button_8 = types.InlineKeyboardButton(text="8")
button_9 = types.InlineKeyboardButton(text="9")


def get_keyboard_main():
    keyboard_main = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    keyboard_main.add(button_search_nearby, button_search_by_name,
                      button_settings, button_set_radius,
                      button_geo, button_help)

    return keyboard_main


def get_keyboard_radius():

    keyboard_radius = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    keyboard_radius.add(button_1, button_2, button_3,
                        button_4, button_5, button_6,
                        button_7, button_8, button_9)

    return keyboard_radius
