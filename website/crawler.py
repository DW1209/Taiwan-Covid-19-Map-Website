import os
import wget
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_datas_url():
    response = requests.get(
        url='https://nidss.cdc.gov.tw/nndss/DiseaseMap?id=19CoV',
        headers={ 'user-agent': UserAgent().random }
    )
    soup = BeautifulSoup(response.text, 'html.parser')
    target = soup.find('a', id='ExcelByArea')
    return target['href']
    

def download_datas(url, filename):
    _ = wget.download(url, filename)


def parse_datas(filename):
    records = dict()

    datas = pd.read_excel(filename, engine='odf', skiprows=8, header=None)
    datas.drop(datas.tail(1).index, inplace=True)

    for i in range(len(datas)):
        name, number = datas[0][i], datas[1][i]
        records[name] = number

    return records


if __name__ == '__main__':
    filename = 'covid19.ods'

    if os.path.exists(filename) == False:
        url = 'https://nidss.cdc.gov.tw' + get_datas_url()
        download_datas(url, filename)

    current_time = float(time.time())
    modification_time = float(os.path.getmtime(filename))
    period_time = current_time - modification_time
    
    if period_time >= 7200.0:
        os.remove(filename)
        url = 'https://nidss.cdc.gov.tw' + get_datas_url()
        download_datas(url, filename)

    records = parse_datas(filename)
    print(records)
