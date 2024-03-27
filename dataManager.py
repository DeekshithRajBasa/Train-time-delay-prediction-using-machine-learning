import re
import requests
from os import system
from bs4 import BeautifulSoup
import csv
import ast
from time import sleep

def webfetch_stations_trains(label):
    data = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    start_urls = {
        'stations': 'https://www.cleartrip.com/trains/stations/list',
        'trains': 'https://www.railyatri.in/time-table'}
    start_url = start_urls[label]

    try:
        print('opening the {} url'.format(label))
        r = requests.get(start_url)
    except requests.exceptions.RequestException as e:
        print('Error fetching URL:', e)
        return None

    soup = BeautifulSoup(r.content, 'html.parser')
    while True:
        table = soup.find_all('table')[0]
        rows = table.find_all('tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            data[re.sub('<.*?>', '', str(cols[0]))] = re.sub('<.*?>', '', str(cols[1]))

        div_lst = soup.find_all('div', {'class': 'pagination'})
        if not len(div_lst):
            break
        a_lst = div_lst[0].find_all('a', {'class': 'next_page'})
        if not len(a_lst):
            break
        r = requests.get('https://www.cleartrip.com' + a_lst[0]['href'])
        soup = BeautifulSoup(r.content, 'html.parser')
    print(label, ' extracted')
    return data


def webfetch_avg_delays(station):
    print(station)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    r = requests.get('https://www.railyatri.in/insights/average-train-delay-at-station/' + station, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = {}
    while True:
        div_lst = soup.find_all('div', {'class': 'pages'})
        if not len(div_lst):
            break
        scripts = soup.find_all('script')
        list_str = re.sub('<.*?>', '', str(scripts[-7])).split(';')[0].split('=')[1].strip()
        train_delay_lst = ast.literal_eval(list_str)
        for train_delay_dict in train_delay_lst:
            mtch = re.match('([0-9]+) \\(([0-9]+).*', train_delay_dict['number'])
            data[mtch.group(1)] = int(mtch.group(2))

        a = div_lst[0].find_all('a')
        if len(a) == 0 or a[1]['title'] == 'No More Data':
            break
        r = requests.get('https://www.railyatri.in' + a[1]['href'], headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
    return data


def update_stations_trains(label):
    data = webfetch_stations_trains(label)
    print(f'updating {label} data')


def filefetch_stations_trains(label):
    data = {}
    print('Compiling {} data'.format(label), end='')
    sleep(5)


def update_avg_delays(stations):
    data = {}
    for station, _ in stations.items():
        data[station] = webfetch_avg_delays(station)


def filefetch_avg_delays():
    data = {}
    print('Computing delay predictions... Please Wait', end='')
    for _ in range(10):
        print('.', end='')
        sleep(1)


if __name__ == '__main__':
    stations = update_stations_trains('stations')
    update_stations_trains('trains')
    stations = filefetch_stations_trains('stations')
    trains = filefetch_stations_trains('trains')
    avg_delays = filefetch_avg_delays()
