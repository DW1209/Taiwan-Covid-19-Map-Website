import wget
import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


area_map = {
    "台北市": "Taipei City",
    "基隆市": "Keelung City",
    "新北市": "New Taipei City",
    "宜蘭縣": "Yilan County",
    "金門縣": "Kinmen County",
    "連江縣": "Lienchiang County",
    "新竹市": "Hsinchu City",
    "桃園市": "Taoyuan City",
    "新竹縣": "Hsinchu County",
    "苗栗縣": "Miaoli County",
    "台中市": "Taichung City",
    "彰化縣": "Chuanghua County",
    "南投縣": "Nantou County",
    "台南市": "Tainan City",
    "嘉義市": "Chiayi City",
    "雲林縣": "Yunlin County",
    "嘉義縣": "Chiayi County",
    "高雄市": "Kaohsiung City",
    "屏東縣": "Pingtung County",
    "澎湖縣": "Penghu County",
    "花蓮縣": "Huanlien County",
    "台東縣": "Taitung County",
    "北區合計": "North Zone Count",
    "中區合計": "Center Zone Count",
    "南區合計": "South Zone Count",
    "東區合計": "East Zone Count",
    "高屏區合計": "Kaoshiung Pingtung Zone Count",
    "台北區合計": "Taipei Zone Count",
    "合計": "Total Count",
}


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
        area, number = datas[0][i], datas[1][i]
        records[area_map[area]] = number

    return records
