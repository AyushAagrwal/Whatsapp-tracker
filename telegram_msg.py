import requests
from dotenv.main import load_dotenv
import os
# from functions import gen_csv
from db import *
import pandas as pd
from analytics_report import *

load_dotenv()
api_key = os.environ['API_key']

def send_msg(chat_id,msg):
    endpoint = f"https://api.telegram.org/bot{api_key}/sendMessage"
    parameters = {'chat_id':chat_id,'text':msg}
    requests.get(url = endpoint, params = parameters)

def gen_csv():
    df = pd.read_sql("select * from info",con)
    df.to_csv("analytics.csv",index=None)

def send_csv(chat_id):
    gen_csv()
    txt = open("analytics.csv" , 'rb')
    url = (f"https://api.telegram.org/bot{api_key}/sendDocument?chat_id={chat_id}")
    url_txt = requests.post(url, files={'document': txt})
    txt.close()
    os.remove("analytics.csv")

def send_qr(chat_id):
    with open("qr.png", "rb") as file:
    # Send the request to Telegram
        url = (f"https://api.telegram.org/bot{api_key}/sendPhoto")
        response = requests.post(url, data={"chat_id": chat_id}, files={"photo": file})
    os.remove("qr.png")

def send_analytics_report(chat_id):
    title = generate_analytics()
    with open("analytics.png", "rb") as file:
    # Send the request to Telegram
        url = (f"https://api.telegram.org/bot{api_key}/sendPhoto")
        response = requests.post(url, data={"chat_id": chat_id, 'caption': title}, files={"photo": file})
    os.remove("analytics.png")

