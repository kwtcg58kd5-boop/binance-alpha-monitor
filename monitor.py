import requests
from bs4 import BeautifulSoup
import os
import json
import hashlib
from datetime import datetime



SERVER_KEY=os.getenv("SERVER_KEY")


CACHE_FILE="cache.json"



def send_wechat(title,msg):

    if not SERVER_KEY:

        return


    url=f"https://sctapi.ftqq.com/{SERVER_KEY}.send"


    requests.post(

        url,

        data={

            "title":title,

            "desp":msg

        }

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

    url="https://alpha123.uk/zh/"


    headers={

        "User-Agent":

        "Mozilla/5.0"

    }


    r=requests.get(

        url,

        headers=headers,

        timeout=20

    )


    soup=BeautifulSoup(

        r.text,

        "html.parser"

    )


    text=soup.get_text(

        "\n"

    )


    return text[:5000]




def get_binance():

    url="https://www.binance.com/zh-CN/support/announcement"


    headers={

        "User-Agent":

        "Mozilla/5.0"

    }


    r=requests.get(

        url,

        headers=headers,

        timeout=20

    )


    return r.text[:5000]




def analyze(text):


    keywords=[

        "Alpha",

        "空投",

        "Airdrop",

        "积分",

        "Points",

        "领取"

    ]


    result=[]


    for k in keywords:


        if k in text:

            result.append(k)



    return result




def main():
    send_wechat(
    "Binance Alpha测试",
    "微信通知链路正常"
)

return

    old=load_cache()


    sources={


        "Alpha123":

        get_alpha123(),



        "Binance官方":

        get_binance()

    }



    for name,text in sources.items():


        keys=analyze(text)



        if len(keys)>=2:


            fingerprint=hashlib.md5(

                text.encode()

            ).hexdigest()



            if fingerprint not in old:


                msg=f"""

🚨 Binance Alpha空投提醒


来源：
{name}


发现关键词：
{','.join(keys)}


时间：
{datetime.now()}


请打开 Binance Alpha 查看


评分：
🔥建议关注


"""


                send_wechat(

                    "🚨 Binance Alpha提醒",

                    msg

                )


                old.append(fingerprint)



    save_cache(old)




if __name__=="__main__":

    main()
