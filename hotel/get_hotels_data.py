from hotel.rapid_api import get_hotel_properties_by_pages, get_photos


# ///Все свойства отелей с API ////
def info_hotels_properties(info_send_dict: dict):
    data_properties = []

    destination_id = info_send_dict['city_id']
    page_size = info_send_dict['count_hotels']
    adults = info_send_dict['amount_people']
    ch_in = info_send_dict['start_date']
    ch_out = info_send_dict['end_date']

    if info_send_dict['command'] == 'bestdeal':
        sort_order = "PRICE"
        page_size = 25  # столько отелей максимум на одной странице
        for page_number in range(1, 9):  # столько страниц  с API Hotels
            cur_data = get_hotel_properties_by_pages(destination_id, page_size, adults, ch_in, ch_out, sort_order, page_number)
            if cur_data is not None:
                data_properties.append(cur_data)
    if info_send_dict['command'] == 'lowprice':
        sort_order = "PRICE"
        page_number = 1  # страница с 25 отелями API Hotels
        cur_data = get_hotel_properties_by_pages(destination_id, page_size, adults, ch_in, ch_out, sort_order, page_number)
        if cur_data is not None:
            data_properties.append(cur_data)
    if info_send_dict['command'] == 'highprice':
        sort_order = "PRICE_HIGHEST_FIRST"
        page_number = 1
        cur_data = get_hotel_properties_by_pages(destination_id, page_size, adults, ch_in, ch_out, sort_order, page_number)
        if cur_data is not None:
            data_properties.append(cur_data)
    return data_properties


def filter_results_hotels(info_send_dict: dict, data_properties: any):
    photo_flag = info_send_dict['show_photos']
    info_hotels_dict = {}
    name = ''
    id_hotel = ""
    count_find_hotels = int(info_send_dict['count_hotels'])
    count_page = 0

    for page in data_properties:
        count_page += 1
        for i in page:
            if count_find_hotels == 0:
                break
            count_find_hotels -= 1
            flag_b_deal = []
            name = i.get('name')
            if name is not None:
                info_hotels_dict.update({name: {}})
            else:
                continue
            if i.get('address') is not None:
                info_hotels_dict[name].update(
                    {'Адрес': str(i['address']['countryName']) + ', ' +
                              str(i['address']['locality']) + ', '
                              + (f'{str(i["address"]["streetAddress"])}, ' if i['address'].get(
                        'streetAddress') is not None else '') + str(
                        i['address']['postalCode'])})
            if i.get('landmarks') is not None:
                dict_distance = {'Расстояние от центра': i['landmarks'][0]['distance']}
                info_hotels_dict[name].update(dict_distance)
                dig_distance = i['landmarks'][0]['distance'].split()[0]
                if info_send_dict['command'] == 'bestdeal':
                    range_distance = info_send_dict['dist_range']
                    if float(range_distance[0]) <= float(dig_distance) <= float(range_distance[1]):
                        flag_b_deal.append(True)
            if i.get('ratePlan') is not None:
                if i['ratePlan'].get('price') is not None:
                    current = i['ratePlan']['price']['current']
                    exactCurrent = i['ratePlan']['price']['exactCurrent']
                    dict_price = {'Цена за ночь': str(exactCurrent) + ' ' + current[0]}
                    info_hotels_dict[name].update(dict_price)
                    if info_send_dict['command'] == 'bestdeal':
                        range_price = info_send_dict['price_range']
                        if float(range_price[0]) <= float(exactCurrent) <= float(range_price[1]):
                            flag_b_deal.append(True)
                    number_of_days = str(info_send_dict['end_date'] - info_send_dict['start_date']).split()[
                        0]
                    sum_exact_Current = round(int(number_of_days) * exactCurrent, 1)
                    info_hotels_dict[name].update(
                        {'Суммарная цена за время пребывания': str(sum_exact_Current) + ' ' + current[0]})
            if len(flag_b_deal) != 2 and info_send_dict[
                'command'] == 'bestdeal':  # если не нашлось подходящего отеля по параметрам bestdeal
                del info_hotels_dict[name]
                count_find_hotels += 1
                continue
            if i.get('id') is not None and photo_flag is True:  # поиск фото отелей
                info_hotels_dict[name].update({'id': i['id']})
                data_photos = get_photos(i['id'])

                if data_photos is not None and 'hotelImages' in data_photos:
                    count = 0
                    for item in data_photos['hotelImages']:
                        url_photo = item['baseUrl'].replace("_{size}", "")
                        count += 1
                        info_hotels_dict[name].update({f'Photo_Url_{count}': url_photo})
                        if count == info_send_dict['count_photos']:
                            break

        if count_find_hotels == 0:
            return info_hotels_dict

        if count_find_hotels == info_send_dict['count_hotels']:
            return 'Отелей с выбранными параметрами не нашлось, '
            'попробуйте изменить диапазоны расстояния и цены'
        elif count_find_hotels != 0:
            return 'Отелей найдено не так много, сколько требовалось'
