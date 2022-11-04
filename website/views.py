import os
import time
from .crawler import *
from flask import Blueprint, render_template


views = Blueprint('views', __name__)


@views.route('/')
def home():
    filename = os.path.join('.', 'website', 'covid19.ods')

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

    return render_template('index.html', records=records)