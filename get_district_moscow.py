# coding=utf-8

import geojson
import shapely.geometry as shg
import requests

print("Загрузка данных: ")
with open('mo.geojson') as f:
    data_gj_mo = geojson.load(f)
print("OK")

def get_district(point):
    
    point = shg.Point(point)
    result = ""
    
    for feature in data_gj_mo['features']:
        polygon = shg.shape(feature['geometry'])
        if polygon.contains(point):
            result = feature['properties']['TYPE_MO'] + ' ' + feature['properties']['NAME']
            break
    return result

def get_coord(address):
    api_url = "https://geocode-maps.yandex.ru/1.x"
    api_key = 'e774a1c0-7bd2-488a-a88d-facab89278a9'
    params = {'geocode': 'Москва ' + address, 'apikey': api_key, 'format': 'json'}
    response = requests.get(api_url, params)
    res = response.json()['response']['GeoObjectCollection'] \
        ['featureMember'][0]['GeoObject']['Point']['pos'].split()
    return [float(res[0]), float(res[1])]

print("""
    ОПРЕДЕЛЕНИЕ МУНИЦИПАЛЬНОГО ОКРУГА МОСКВЫ ПО АДРЕСУ

    Адрес необходимо ввести без указания города Москва
    (иначе можно получить неверные результаты).
    В программе используются данные районов с сайта 
    https://gis-lab.info/qa/moscow-atd.html,
    а также Геокодер API Яндекс.Карт.
""")

finish = True
while finish:
    address = input("\nВведите адрес (например, Охотный ряд 1): ")
    if len(address) > 0:
        print(get_district(get_coord(address)))
    check = input("\nПродолжить? (yes, да / [no, нет]): ")
    if check != 'yes' and check != 'да':
        finish = False
