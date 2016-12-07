from googleplaces import GooglePlaces, types
import googlemaps
import admin

g_places = GooglePlaces(admin.google_API_key)
g_maps = googlemaps.Client(key=admin.google_API_key)

default_radius_by_name = 40000
message_max_size = 12


def search_nearby(latitude, longitude, radius):

    coordinates_str = str(latitude) + ', ' + str(longitude)

    query_result = g_places.nearby_search(
        location=coordinates_str, keyword='Кинотеатр',
        radius=radius, rankby='prominence', types=[types.TYPE_MOVIE_THEATER])

    location_list = g_maps.reverse_geocode((latitude, longitude))

    answer = generate_answer_search(query_result)
    if answer is None:

        return 'По Вашему запросу ничго не найдено'

    answer += '*/- Кинотеатры в радиусе ' + str(radius / 1000) + ' км.\n'
    answer += 'Ваше местоположение:\n' + location_list[0]['formatted_address'] + '\n'

    return answer


def search_by_name(latitude, longitude, name_theater):

    coordinates_str = str(latitude) + ', ' + str(longitude)

    query_result = g_places.nearby_search(
        location=coordinates_str, keyword='Кинотеатр', name=name_theater,
        radius=default_radius_by_name, rankby='distance', types=[types.TYPE_MOVIE_THEATER])

    location_list = g_maps.reverse_geocode((latitude, longitude))

    answer = generate_answer_search(query_result)
    if answer is None:

        return 'По Вашему запросу ничго не найдено'

    answer += '*/- Кинотеатры ' + name_theater + ' в радиусе ' + str(default_radius_by_name / 1000) + ' км.\n'
    answer += 'Ваше местоположение:\n' + location_list[0]['formatted_address'] + '\n'

    return answer


def cur_location_and_radius_message(latitude, longitude, radius):

    location_list = g_maps.reverse_geocode((latitude, longitude))

    message = 'Ваше местоположение:\n' + location_list[0]['formatted_address'] + '\n'
    message += 'Производится поиск кинотеатров в радиусе ' + str(radius / 1000) + ' км.:\n'

    return message


def cur_location_and_name_message(latitude, longitude, name_theater):

    location_list = g_maps.reverse_geocode((latitude, longitude))

    message = 'Ваше местоположение:\n' + location_list[0]['formatted_address'] + '\n'
    message += 'Производится поиск кинотеатра ' + name_theater + ' в радиусе ' + \
               str(default_radius_by_name / 1000) + ' км.:\n'

    return message


def generate_answer_search(query_result):

    if len(query_result.places) is 0:

        return None

    answer = 'Результат поиска: /*\n'

    cnt = 0
    for place in query_result.places:

        if cnt >= message_max_size:

            return answer

        cnt += 1

        name = place.name   # Returned places from a query are place summaries.
        if name is not None:

            answer += name + '\n'
        else:

            answer += 'Name: undefined \n'

        place.get_details()     # The following method has to make a further API call.

        address = place.formatted_address
        if address is not None:

            answer += 'Адрес: ' + place.formatted_address + '\n'
        else:

            answer += 'Адрес: undefined\n'

        phone_number = place.international_phone_number
        if phone_number is not None:

            answer += 'Телефон: ' + place.international_phone_number + '\n'
        else:

            answer += 'Телефон: undefined\n'

        website = place.website
        if website is not None:

            answer += 'Сайт: ' + place.website + '\n'
        else:

            answer += 'Сайт: undefined\n'

        url = place.url
        if url is not None:

            answer += 'Карта: ' + place.url + '\n'
        else:

            answer += 'Карта: undefined\n'

        rating = place.rating
        if rating is not '':

            answer += 'Рейтинг: ' + str(rating) + '/5.0' + '\n'
        else:

            answer += 'Рейтинг: undefined\n'

        answer += '\n'

    return answer

