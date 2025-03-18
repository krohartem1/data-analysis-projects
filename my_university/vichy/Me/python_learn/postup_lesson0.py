import requests
from time import sleep

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from geopy.distance import geodesic

moscow_center = (55.7558, 37.6173)
mkad_radius_km = 15

all_vacancies = [
    {
        "name": "Аналитик данных",
        "address": {"lat": 55.7522, "lng": 37.6156},
    },  # в пределах МКАД
    {
        "name": "Программист",
        "address": {"lat": 56.0000, "lng": 38.0000},
    },  # за пределами МКАД
    {
        "name": "Менеджер",
        "address": {"lat": 55.7400, "lng": 37.5200},
    },  # в пределах МКАД
]


def inside_mkad(vacancie_lat, vacancie_lng):
    vacancy_coords = (vacancie_lat, vacancie_lng)
    dist_to_center = geodesic(moscow_center, vacancy_coords).km
    return dist_to_center <= mkad_radius_km


for vac in all_vacancies:
    if "address" in vac and vac["address"] != None:
        print(vac["address"]["lat"], ":::", vac["address"]["lng"])
vacancies_inside_mkad = [
    vac
    for vac in all_vacancies
    if "address" in vac
    and vac["address"] != None
    and inside_mkad(vac["address"]["lat"], vac["address"]["lng"])
]
print(len(vacancies_inside_mkad))
