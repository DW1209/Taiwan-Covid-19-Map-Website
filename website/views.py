import os
import time
from .crawler import *
from flask import Blueprint, render_template


views = Blueprint('views', __name__)


@views.route('/')
def home():
    records, ranges = get_records_and_ranges()
    return render_template('index.html', records=records, ranges=ranges)