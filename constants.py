from main import default_radius_nearby

about_message = "Это бот Kinonaizer.\n" \
               "C его помощью можно легко искать кинотеатры поблизости.\n"

help_message = "Введите команду /settings для просмотра текущих настроек по поиску ближайших кинотеатров\n" \
               "/set_radius - установить радиус поиска кинотеатров\n" \
               "(default radius = " + str(default_radius_nearby / 1000) + " км.)\n" + \
               "/search_nearby - Найти кинотеатры поблизости\n" \
               "/search_by_name - Найти кинотеатр по названию"

insert_radius_message = "Введите радиус поиска в километрах от 1 до 10"

insert_radius_message_bad_range = "Error: Bad input data range\n" \
                                  "Radius should be in the range [1:10]"

error_input_integer = "Error: Bad input data\n" \
                      "Please enter an integer"

insert_name_theater = "Введите название кинотеатра"

success_inp_data = "Successfully input data!"

happy_birthday = "Администрация Kinonaizer от всего сердца поздравляет вас с днём рождения ;)\n" \
                 "Желаем вам успехов и побольше свободного времени, " \
                 "чтобы вы могли искать здесь кинотеатры и ходить туда вместе со своими близкими!"
