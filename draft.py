from dataclasses import dataclass


@dataclass
class ResultData:
    names: list
    addresses: list
    center_distances: list
    prices: list
    hotel_ids: list
    photos_links: list


resultdata = ResultData([], [], [], [], [], [[] for i in range(4)])
print(resultdata.photos_links)
