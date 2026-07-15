import os
import json
import hashlib
import requests

from datetime import datetime

from playwright.sync_api import sync_playwright



SERVER_KEY = os.getenv("SERVER_KEY")


CACHE_FILE = "cache.json"



def send_wechat(title,msg):

    if not SERVER_KEY:

        return


    url = f"https://sctapi.ftqq.com/{SERVER_KEY}.send"


    requests.post(

        url,

        data={

            "title":title,

            "desp":msg

        },

        timeout=10

    )



def load_cache():

    try:

        with open(CACHE_FILE) as f:

            return json.load(f)

    except:

        return []



def save_cache(data):

    with open(CACHE_FILE,"w") as f:

        json.dump(data,f)



def get_alpha123():



    with sync_playwright() as p:


        browser=p.chromium.launch(

            headless=True

        )


        page=browser.new_page()



        page.goto(

            "https://alpha123.uk/zh/",

            wait_until="networkidle",

            timeout=60000

        )


        text=page.inner_text("body")



        browser.close()



    return text




def get_binance():


    url="https://www.binance.com/zh-CN/support/announcement"



    r=requests.get(

        url,

        headers={

            "User-Agent":

            "Mozilla/5.0"

        },

        timeout=20

    )


    return r.text




def analyze(text):


    keywords=[

        "Alpha",

        "空投",

        "Airdrop",

        "Points",

        "积分",

        "领取"

    ]


    result=[]


    for k in keywords:


        if k in text:

            result.append(k)



    return result




def main():



    cache=load_cache()



    sources={


        "Alpha123":

        get_alpha123(),


        "Binance官方":

        get_binance()


    }



    for name,text in sources.items():



        keys=analyze(text)



        if len(keys)>=3:



            fingerprint=hashlib.md5(

                text.encode()

            ).hexdigest()



            if fingerprint not in cache:



                msg=f"""

🚨 Binance Alpha 空投提醒


来源：

{name}


发现：

{','.join(keys)}


检测时间：

{datetime.now()}


请打开 Binance Alpha 查看


🔥建议：

关注领取时间和 Alpha Points 要求


"""


                send_wechat(

                    "🚨 Binance Alpha提醒",

                    msg

                )



                cache.append(fingerprint)



    save_cache(cache)




if __name__=="__main__":

    main()
