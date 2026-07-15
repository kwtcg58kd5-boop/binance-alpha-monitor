import requests
from bs4 import BeautifulSoup
import os
import json
import hashlib
from datetime import datetime


SERVER_KEY = os.getenv("SERVER_KEY")

CACHE_FILE = "cache.json"


def send_wechat(title, msg):

    if not SERVER_KEY:
        print("没有找到 SERVER_KEY")
        return


    url = f"https://sctapi.ftqq.com/{SERVER_KEY}.send"


    try:

        r = requests.post(
            url,
            data={
                "title": title,
                "desp": msg
            },
            timeout=10
        )

        print(r.text)


    except Exception as e:

        print("微信发送失败:", e)



def load_cache():

    try:

        with open(CACHE_FILE, "r") as f:

            return json.load(f)

    except:

        return []



def save_cache(data):

    with open(CACHE_FILE, "w") as f:

        json.dump(data, f)



def get_alpha123():

    url = "https://alpha123.uk/zh/"


    headers = {

        "User-Agent":
        "Mozilla/5.0"

    }


    r = requests.get(
        url,
        headers=headers,
        timeout=20
    )


    soup = BeautifulSoup(
        r.text,
        "html.parser"
    )


    return soup.get_text("\n")



def get_binance():

    url = "https://www.binance.com/zh-CN/support/announcement"


    headers = {

        "User-Agent":
        "Mozilla/5.0"

    }


    r = requests.get(
        url,
        headers=headers,
        timeout=20
    )


    return r.text



def analyze(text):

    keywords = [

        "Alpha",
        "空投",
        "Airdrop",
        "积分",
        "Points",
        "领取"

    ]


    result = []


    for k in keywords:

        if k in text:

            result.append(k)


    return result



# ==========================
# 测试区域
# ==========================

def main():


    # 测试微信通知
    # 测试成功后删除这几行

    send_wechat(
        "Binance Alpha测试",
        "GitHub + Server酱 微信通知测试成功"
    )


    return



# ==========================
# 正式运行入口
# ==========================

if __name__ == "__main__":

    main()
