import json
import re
from typing import Any

from config_data.config import URL_LOC_SEARCH, HEADERS, URL_PHOTOS, URL_PROPERTIES
from utils.request import request_get


def get_city_api(city):
    destnation_id_city = None
    querystring_loc_search = {"query": city, "locale": "en_US", "currency": "USD"}
    response = request_get(URL_LOC_SEARCH, HEADERS, querystring_loc_search)
    if response is not None:
        pattern = r'(?<="CITY_GROUP",).+?[\]]'
        find = re.search(pattern, response)
        result = None
        if find:
            result = json.loads(f"{{{find[0]}}}")
        if result is not None:
            for entity in result["entities"]:
                if entity['type'] == 'CITY' and entity['name'] == city:
                    destnation_id_city = entity['destinationId']
                else:
                    break
    return destnation_id_city


def get_hotel_properties_by_pages(destination_id: Any, page_size: int, adults: str, ch_in: str, ch_out: str,
                                  sort_order: str, page_number: int, url=URL_PROPERTIES) -> dict:
    querystring_properties = {"destinationId": destination_id, "pageNumber": str(page_number),
                              "pageSize": page_size, "checkIn": ch_in, "checkOut": ch_out,
                              "adults1": adults, "sortOrder": sort_order, "locale": "en_US", "currency": "USD"}
    response = request_get(url, HEADERS, querystring_properties)

    if response is not None:
        pattern = r'(?<="results":)(.*)(?=,"pagination":)'
        find = re.search(pattern, response)
        if find is not None:
            return json.loads(find[0])


def get_photos(id_hotel):
    querystring_photos = {"id": str(id_hotel)}
    response = request_get(URL_PHOTOS, HEADERS, querystring_photos)
    if response is not None:
        data_photos = json.loads(response)
        if data_photos is not None:
            return data_photos
