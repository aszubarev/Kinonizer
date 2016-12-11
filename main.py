"""
29/11/2016
"""
import telebot
import constants
import admin
import datetime
import googlemaps
import logging
import UsersDB
import pymysql
from searcher import search_nearby
from searcher import search_by_name
from searcher import cur_location_and_radius_message
from searcher import cur_location_and_name_message
from keyboard import get_keyboard_main
from keyboard import get_keyboard_radius

g_maps = googlemaps.Client(key=admin.google_API_key)

bot = telebot.TeleBot(admin.token)

logging.basicConfig(filename='log_err.log', level=logging.ERROR,
                    format='\n#######################################################################################\n'
                           '%(asctime)s - %(levelname)s - %(message)s')

db = pymysql.connect(user=admin.connectDB_user, passwd=admin.connectDB_passwd,
                     host=admin.connectDB_host, port=admin.connectDB_port, db=admin.connectDB_name)
db.set_charset('utf8')
db.autocommit(True)

default_radius_nearby = 3000

flag_quick_start = dict()          # Key = id, Value = True or False
flag_insert_radius = dict()        # Key = id, Value = True or False
flag_insert_name_theater = dict()  # Key = id, Value = True or False

keyboard_main = get_keyboard_main()
keyboard_radius = get_keyboard_radius()


def my_logger(message, answer, logfile):
    logfile.write("\n----------------\n")

    if message.from_user.last_name is not None:

        logfile.write("Сообщение от {0} {1}. (id = {2})\n Текст = {3}\n".format(message.from_user.first_name,
                                                                                message.from_user.last_name,
                                                                                str(message.from_user.id),
                                                                                message.text))
    else:

        logfile.write("Сообщение от {0}. (id = {1})\n Текст = {2}\n".format(message.from_user.first_name,
                                                                            str(message.from_user.id),
                                                                            message.text))

    logfile.write(str(datetime.datetime.now().replace(microsecond=0)) + "\n")
    logfile.write("Answer = " + answer + "\n")


@bot.message_handler(commands=['start'])
def print_start(message):

    admin.message_new_user(bot, message)

    UsersDB.insert_user(db, message.chat.id, message.from_user.first_name, default_radius_nearby)
    if message.from_user.last_name is not None:

        UsersDB.update_last_name(db, message.chat.id, message.from_user.last_name)

    bot.send_message(message.chat.id, "Прикрепите своё местоположение", reply_markup=keyboard_main)
    flag_quick_start[message.chat.id] = True


@bot.message_handler(commands=['about'])
def print_settings(message):

    bot.send_message(message.chat.id, constants.about_message, reply_markup=keyboard_main)


@bot.message_handler(commands=['help'])
def print_help(message):

    bot.send_message(message.chat.id, constants.help_message, reply_markup=keyboard_main)


@bot.message_handler(commands=['search_nearby'])
def print_search_nearby(message):

    # ignore if already exist
    UsersDB.insert_user(db, message.chat.id, message.from_user.first_name, default_radius_nearby)

    latitude, longitude = UsersDB.select_location(db, message.chat.id)
    if latitude is None and longitude is None:

        bot.send_message(message.chat.id, "Прикрепите своё местоположение", reply_markup=keyboard_main)
        flag_quick_start[message.chat.id] = True

    else:

        first_message = cur_location_and_radius_message(latitude, longitude,
                                                        UsersDB.select_radius_nearby(db, message.chat.id))
        bot.send_message(message.chat.id, first_message, reply_markup=keyboard_main)

        answer = search_nearby(latitude, longitude, UsersDB.select_radius_nearby(db, message.chat.id))
        bot.send_message(message.chat.id, answer, reply_markup=keyboard_main)


@bot.message_handler(commands=['search_by_name'])
def print_search_by_name(message):

    # ignore if already exist
    UsersDB.insert_user(db, message.chat.id, message.from_user.first_name, default_radius_nearby)

    latitude, longitude = UsersDB.select_location(db, message.chat.id)
    if latitude is None and longitude is None:

        bot.send_message(message.chat.id, "Прикрепите своё местоположение", reply_markup=keyboard_main)
        flag_quick_start[message.chat.id] = True

    else:

        bot.send_message(message.chat.id, constants.insert_name_theater, reply_markup=keyboard_main)
        flag_insert_name_theater[message.chat.id] = True


@bot.message_handler(commands=['settings'])
def print_settings(message):

    # ignore if already exist
    UsersDB.insert_user(db, message.chat.id, message.from_user.first_name, default_radius_nearby)

    latitude, longitude = UsersDB.select_location(db, message.chat.id)
    if latitude is None and longitude is None:

        bot.send_message(message.chat.id, "Прикрепите своё местоположение", reply_markup=keyboard_main)
        flag_quick_start[message.chat.id] = True

    else:

        location_list = g_maps.reverse_geocode((latitude, longitude))
        answer = "Ваше местоположение:\n" + location_list[0]['formatted_address'] + '\n'
        answer += "(Для смены просто прикрепите своё местоположение)\n\n"
        answer += "Радиус поиска = " + str(UsersDB.select_radius_nearby(db, message.chat.id) / 1000) + " км." + "\n"
        answer += "(Для смены: /set_radius)"

    bot.send_message(message.chat.id, answer, reply_markup=keyboard_main)


@bot.message_handler(commands=['set_radius'])
def set_radius(message):

    # ignore if already exist
    UsersDB.insert_user(db, message.chat.id, message.from_user.first_name, default_radius_nearby)

    bot.send_message(message.chat.id, constants.insert_radius_message, reply_markup=keyboard_radius)
    flag_insert_radius[message.chat.id] = True


@bot.message_handler(commands=['time'])
def stop(message):

    now_time = datetime.datetime.now().time()
    bot.send_message(message.chat.id, now_time.replace(microsecond=0), reply_markup=keyboard_main)


@bot.message_handler(content_types=['location'])
def print_location(message):

    # ignore if already exist
    UsersDB.insert_user(db, message.chat.id, message.from_user.first_name, default_radius_nearby)

    UsersDB.update_location(db, message.chat.id, float(message.location.latitude), float(message.location.longitude))

    if flag_quick_start.get(message.chat.id) is None or flag_quick_start.get(message.chat.id) is False:

        bot.send_message(message.chat.id, constants.success_inp_data, reply_markup=keyboard_main)
        flag_quick_start[message.chat.id] = False

    else:   # Quick start

        first_message = cur_location_and_radius_message(message.location.latitude,
                                                        message.location.longitude,
                                                        UsersDB.select_radius_nearby(db, message.chat.id))

        bot.send_message(message.chat.id, first_message, reply_markup=keyboard_main)

        answer = search_nearby(message.location.latitude,
                               message.location.longitude,
                               UsersDB.select_radius_nearby(db, message.chat.id))
        bot.send_message(message.chat.id, answer, reply_markup=keyboard_main)

        flag_quick_start[message.chat.id] = False


@bot.message_handler(content_types=['text'])
def dialog(message):

    if flag_insert_radius.get(message.chat.id) is True:

        try:

            if int(message.text) > 9 or int(message.text) < 1:

                bot.send_message(message.chat.id, constants.insert_radius_message_bad_range, reply_markup=keyboard_main)

            else:

                UsersDB.update_radius_nearby(db, message.chat.id, float(message.text) * 1000)
                bot.send_message(message.chat.id, constants.success_inp_data, reply_markup=keyboard_main)

        except ValueError:   # Handle the exception

            bot.send_message(message.chat.id, constants.error_input_integer, reply_markup=keyboard_main)

        flag_insert_radius[message.chat.id] = False

    elif flag_insert_name_theater.get(message.chat.id) is True:

        if len(message.text) > 20:

            bot.send_message(message.chat.id, "ERROR: подозрительно длинное название", reply_markup=keyboard_main)

        elif len(message.text) < 3:

            bot.send_message(message.chat.id, "ERROR: подозрительно короткое название", reply_markup=keyboard_main)

        else:

            flag_insert_name_theater[message.chat.id] = False

            latitude, longitude = UsersDB.select_location(db, message.chat.id)

            first_message = cur_location_and_name_message(latitude, longitude, message.text)
            bot.send_message(message.chat.id, first_message, reply_markup=keyboard_main)

            answer = search_by_name(latitude, longitude, message.text)
            bot.send_message(message.chat.id, answer, reply_markup=keyboard_main)

        flag_insert_name_theater[message.chat.id] = False

    else:   # Echo

        if message.chat.id != admin.admin_telegram_id:

            if message.from_user.last_name is not None:

                bot.send_message(admin.admin_telegram_id, message.from_user.first_name + " " +
                                 message.from_user.last_name + admin.send_message + message.text,
                                 reply_markup=keyboard_main)
            else:

                bot.send_message(admin.admin_telegram_id, message.from_user.first_name + " " +
                                 admin.send_message + message.text, reply_markup=keyboard_main)

        bot.send_message(message.chat.id, "Echo:\n" + message.text, reply_markup=keyboard_main)

        log_filename = "log.txt"
        logfile = open(log_filename, "a")
        my_logger(message, message.text, logfile)
        logfile.close()


if __name__ == '__main__':

    try:

        bot.polling(none_stop=True, interval=0)

    except:

        logging.exception('')
        raise
