import logging
import time
import aiohttp
import json
from dataclasses import dataclass
from data import config


@dataclass
class ResultData:
    names: list
    addresses: list
    center_distances: list
    prices: list
    hotel_ids: list
    photos_links: list


async def lp_get(data: dict, username: str) -> ResultData:
    querystring_cities = {"query": f"{data['city']}", "locale": "en_US"}
    headers = {
        "X-RapidAPI-Key": f"{config.API_TOKEN}",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    }
    session = aiohttp.ClientSession()
    resultdata = ResultData([], [], [], [], [], [[] for _ in range(data['hotels_amount'])])


    logging.info(f'User: {username} started city search')
    start_time_city = time.time()
    async with session.get('https://hotels4.p.rapidapi.com/locations/v2/search', headers=headers,
                           params=querystring_cities) as response:
        time_city = round(time.time() - start_time_city, 3)
        logging.info(f'User: {username} finished city search, code: {response.status}, time: {time_city}')
        html = await response.text()
        resp_json = json.loads(html)
        destinationId = resp_json['suggestions'][0]['entities'][0]['destinationId']



    querystring_hotels = {"destinationId": f"{destinationId}", "pageNumber": "1", "pageSize": "25", "checkIn": f"{data['checkin']}",
                   "checkOut": f"{data['checkout']}", "adults1": "1", "sortOrder": f"{data['hotels_sort'] if data['hotels_sort'] != 'BEST_DEAL' else 'PRICE'}",
                   "locale": "en_US", "currency": "USD"}

    logging.info(f'User: {username} started hotels search')
    start_time_hotels = time.time()


    async with session.get('https://hotels4.p.rapidapi.com/properties/list', headers=headers,
                           params=querystring_hotels) as response:
        time_hotels = round(time.time() - start_time_hotels, 3)
        logging.info(f'User: {username} finished hotels search, code: {response.status}, time: {time_hotels}')
        html = await response.text()
        resp_json = json.loads(html)

        request_results = resp_json['data']['body']['searchResults']['results']

        # цена не уб, расст до центра не уб.

        if data['hotels_sort'] == 'BEST_DEAL':
            request_results.sort(key=lambda x: float(x['landmarks'][0]['distance'].replace(' miles', '')))
            request_results.sort(key=lambda x: x['ratePlan']['price']['current'])



        for i in range(data['hotels_amount']):
            name = request_results[i]['name']
            hotel_id = request_results[i]['id']
            address = request_results[i]['address']['streetAddress']
            center_distance = request_results[i]['landmarks'][0]['distance']
            price = request_results[i]['ratePlan']['price']['current']



            resultdata.names.append(name)
            resultdata.hotel_ids.append(hotel_id)
            resultdata.addresses.append(address)
            resultdata.center_distances.append(center_distance)
            resultdata.prices.append(price)


        if data['photos'] > 0:
            logging.info(f'User: {username} started photos search')
            start_time_photos = time.time()

            for i in range(data['hotels_amount']):
                hotel_id = resultdata.hotel_ids[i]

                photo_resp = await session.get('https://hotels4.p.rapidapi.com/properties/get-hotel-photos', headers=headers, params={"id": f"{hotel_id}"})
                html = await photo_resp.text()
                photo_resp_json = json.loads(html)

                for j in range(data['photos']):
                    cur_photo = photo_resp_json['hotelImages'][j]['baseUrl']
                    resultdata.photos_links[i].append(cur_photo.replace('{size}', 'z'))

            time_photos = round(time.time() - start_time_photos, 3)
            logging.info(f'User: {username} finished hotels search, code: {response.status}, time: {time_photos}')
        logging.info(f'User: {username} finished search, total time: {round(time_hotels + time_city + (time_photos if  data["photos"] > 0 else 0), 3)}')





    await session.close()
    return resultdata

