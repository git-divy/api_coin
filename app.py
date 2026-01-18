from flask import Flask, request, jsonify, render_template, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from aliver import keep_alive
import json
from tabulator import tabulate
import os
import requests
from tabulator import tabulate
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get('API_KEY')
app = Flask(__name__)


# Setting up Schedulars
scheduler = BackgroundScheduler()
scheduler.add_job(
    id="aliver",
    func=keep_alive,
    args=(None,),
    trigger="interval",
    seconds=10 * 60,
)

import requests
import json

COINS = [
    "bitcoin",
    "ethereum",
    "tether",
    "binancecoin",
    "solana",
    "ripple",
    "cardano",
    "dogecoin",
    "polkadot",
    "tron"
]

def get_data():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": ",".join(COINS),
        "vs_currencies": "usd"
    }

    headers = {
        "x-cg-demo-api-key": API_KEY
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        dat = []
        data = response.json()
        for d in data:
            chunk = {}
            chunk['id'] = d
            chunk['price'] = '$ '+ str(data[d]['usd'])
            dat.append(chunk)

        return dat  # Pretty JSON output

    else:
        return None



@app.route("/")
def index():
    datax = get_data()
    tab_data = tabulate(datax=datax, dump=True)
    css = """
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap");
        
        :root {
            --md-sys-color-primary: #d0bcff;
            --md-sys-color-primary-container: #4f378b;
            --md-sys-color-on-primary: #371e73;
            --md-sys-color-on-primary-container: #eaddff;
            --md-sys-color-surface: #10100f;
            --md-sys-color-on-surface: #e6e1e5;
            --md-sys-color-outline: #938f99;
            --md-sys-shape-corner-medium: 12px;
            --md-sys-elevation-level1: 0px 1px 2px 0px rgba(0, 0, 0, 0.3),
                0px 1px 3px 1px rgba(0, 0, 0, 0.15);
        }
        
        body {
            font-family: "Roboto", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background-color: var(--md-sys-color-surface);
            color: var(--md-sys-color-on-surface);
            padding: 24px;
            margin: 0;
            line-height: 1.5;
        }
        
        pre {
            color: var(--md-sys-color-primary);
            font-size: 18px;
            font-weight: 400;
            margin-bottom: 24px;
            margin-top: 0;
        }

        h2 {
            color: var(--md-sys-color-primary);
            font-size: 28px;
            font-weight: 400;
            margin-bottom: 24px;
            margin-top: 0;
        }
        
    </style>
    """

    
    return f"{css}<h2>API PREVIEW (/api)<h2><pre>{tab_data}</pre>"



@app.route("/start")
def start():
    try:
        if scheduler.running:
            return "Scheduler is already running"

        scheduler.modify_job(job_id="aliver", args=(request.host_url,))
        scheduler.start()
        return f"Schedular has started."

    except Exception as e:
        return str(e)


@app.route("/api", methods=["GET"])
def get_available_filters():
    try:
        return get_data(), 200
    except Exception as e:
        return {'error' : str(e)}, 400


@app.route("/res/<path:filename>")
def serve_res_files(filename):
    return send_from_directory("res", filename)

if __name__ == "__main__":
    app.run()
