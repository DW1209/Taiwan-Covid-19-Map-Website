import os
import re
import csv
import json
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


area_map = {
    '台北市': 'Taipei City',
    '基隆市': 'Keelung City',
    '新北市': 'New Taipei City',
    '宜蘭縣': 'Yilan County',
    '金門縣': 'Kinmen County',
    '連江縣': 'Lienchiang County',
    '新竹市': 'Hsinchu City',
    '桃園市': 'Taoyuan City',
    '新竹縣': 'Hsinchu County',
    '苗栗縣': 'Miaoli County',
    '台中市': 'Taichung City',
    '彰化縣': 'Chuanghua County',
    '南投縣': 'Nantou County',
    '台南市': 'Tainan City',
    '嘉義市': 'Chiayi City',
    '雲林縣': 'Yunlin County',
    '嘉義縣': 'Chiayi County',
    '高雄市': 'Kaohsiung City',
    '屏東縣': 'Pingtung County',
    '澎湖縣': 'Penghu County',
    '花蓮縣': 'Huanlien County',
    '台東縣': 'Taitung County',
    '總計': 'Total Count'
}


def web_crawling(patients_filename, ranges_filename):
    response = requests.get(
        url='https://nidss.cdc.gov.tw/nndss/DiseaseMap?id=19CVS',
        headers={ 'user-agent': UserAgent().random }
    )
    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.find('script', string=lambda x: x and 'hmJson.push(' in x).string
    sidx = content.find('hmJson.push(') + len('hmJson.push(')
    eidx = content.find(');', sidx)
    content = content[sidx:eidx].strip()
    data = json.loads(content)
    records = read_patients_datas(data)
    store_patients_datas(records, patients_filename)
    records = parse_patients_datas(patients_filename)

    regex = re.compile(r'"dataClasses".*"regionName')
    target = str(soup.find("div", id='appendContainer'))
    ranges = eval(str(regex.search(target).group(0))[14:-12])
    ranges = read_ranges_datas(ranges)
    store_ranges_datas(ranges, ranges_filename)
    ranges = parse_ranges_datas(ranges_filename)

    return records, ranges


def read_patients_datas(data):
    records = dict()
    for entry in data['series']:
        area, number = entry['code'], entry['value']
        records[area_map[area]] = number
    return records


def parse_patients_datas(filename):
    records = dict()
    datas = pd.read_csv(filename, sep=',', encoding='utf-8')
    for i in range(len(datas)):
        records[datas['Area'][i]] = int(datas['Number'][i])
    return records


def read_ranges_datas(ranges):
    df = pd.DataFrame()
    df['from'] = [dict(value)['from'] for value in ranges]
    df['to'] = [dict(value)['to'] for value in ranges]
    return df


def parse_ranges_datas(filename):
    ranges = dict()
    datas = pd.read_csv(filename, sep=',', encoding='utf-8')
    for i in range(len(datas)):
        ranges[i + 1] = {"from": int(datas['from'][i]), "to": int(datas['to'][i])}
    return ranges


def store_patients_datas(records, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Area', 'Number'])
        for area, number in records.items():
            writer.writerow([area, number])


def store_ranges_datas(ranges, filename):
    ranges.to_csv(filename, sep=',', encoding='utf-8')


def get_records_and_ranges():
    base = os.path.dirname(__file__)
    ranges_filename = os.path.join(base, 'ranges.csv')
    patients_filename = os.path.join(base, 'covid19.csv')

    if not os.path.exists(patients_filename) or not os.path.exists(ranges_filename):
        records, ranges = web_crawling(patients_filename, ranges_filename)
        return records, ranges

    current_time = float(time.time())
    modification_time = float(os.path.getmtime(patients_filename))
    period_time = current_time - modification_time
    
    if period_time >= 7200.0:
        os.remove(ranges_filename)
        os.remove(patients_filename)
        records, ranges = web_crawling(patients_filename, ranges_filename)
    else:
        ranges = parse_ranges_datas(ranges_filename)
        records = parse_patients_datas(patients_filename)

    return records, ranges
