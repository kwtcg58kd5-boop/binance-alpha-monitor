import os
import json
import hashlib
import requests
import re

from datetime import datetime

from playwright.sync_api import sync_playwright



SERVER_KEY = os.getenv("SERVER_KEY")

CACHE_FILE = "cache.json"



# =====================
# Server酱微信通知
# =====================

def send_wechat(title, content):

    if not SERVER_KEY:

        print("SERVER_KEY不存在")

        return


    try:

        url = f"https://sctapi.ftqq.com/{SERVER_KEY}.send"


        r = requests.post(

            url,

            data={

                "title": title,

                "desp": content

            },

            timeout=10

        )


        print(r.text)


    except Exception as e:

        print("微信发送失败:", e)




# =====================
# 缓存
# =====================

def load_cache():

    try:

        with open(CACHE_FILE,"r") as f:

            return json.load(f)


    except:

        return []




def save_cache(data):

    with open(CACHE_FILE,"w") as f:

        json.dump(data,f)




# =====================
# Alpha123抓取
# =====================

def get_alpha123():

    text=""


    try:

        with sync_playwright() as p:


            browser=p.chromium.launch(

                headless=True

            )


            page=browser.new_page()



            page.goto(

                "https://alpha123.uk/zh/",

                wait_until="domcontentloaded",

                timeout=30000

            )


            page.wait_for_timeout(5000)



            text=page.inner_text("body")



            browser.close()



    except Exception as e:

        print("Alpha123失败:",e)



    return text





# =====================
# Binance公告
# =====================

def get_binance():

    try:

        r=requests.get(

            "https://www.binance.com/zh-CN/support/announcement",

            headers={

                "User-Agent":

                "Mozilla/5.0"

            },

            timeout=20

        )


        return r.text


    except:

        return ""





# =====================
# 提取积分
# =====================

def get_points(text):


    patterns=[

        r"(\d+)\s*Alpha Points",

        r"(\d+)\s*Points",

        r"(\d+)\s*积分"

    ]


    for p in patterns:


        m=re.search(

            p,

            text,

            re.I

        )


        if m:

            return m.group(1)



    return "未知"





# =====================
# 提取时间
# =====================

def get_time(text):


    patterns=[

        r"\d{1,2}:\d{2}",

        r"\d{4}[-/]\d{1,2}[-/]\d{1,2}"

    ]


    for p in patterns:


        m=re.search(

            p,

            text

        )


        if m:

            return m.group(0)



    return "未知"





# =====================
# 判断价值
# =====================

def evaluate(text):


    score=5


    reasons=[]



    words=[

        "AI",

        "DeFi",

        "RWA",

        "Layer",

        "BTC",

        "ETH"

    ]



    for w in words:


        if w.lower() in text.lower():

            score+=1

            reasons.append(w)



    if score>=8:

        result="🔥值得重点关注"


    elif score>=6:

        result="✅可以参与"


    else:

        result="⚠️看积分决定"



    return score,result





# =====================
# 主程序
# =====================

def main():


    cache=load_cache()



    sources={

        "Alpha123":

        get_alpha123(),



        "Binance官方":

        get_binance()

    }



    keywords=[

        "Alpha",

        "Airdrop",

        "空投",

        "Points",

        "积分",

        "领取"

    ]



    for source,text in sources.items():


        if not text:

            continue



        count=sum(

            1 for k in keywords

            if k.lower() in text.lower()

        )



        if count < 3:

            continue



        fingerprint=hashlib.md5(

            text.encode("utf-8")

        ).hexdigest()



        if fingerprint in cache:

            continue



        points=get_points(text)

        time=get_time(text)

        score,result=evaluate(text)



        message=f"""

🚨 Binance Alpha 空投提醒


来源：

{source}


⏰ 时间：

{time}


⭐ Alpha Points：

{points}


🔥评分：

{score}/10


判断：

{result}


💰预计价值：

仅供参考


检测时间：

{datetime.now()}


请及时打开 Binance Alpha 查看


"""



        send_wechat(

            "🚨 Binance Alpha提醒",

            message

        )


        cache.append(fingerprint)



    save_cache(cache)




if __name__=="__main__":

    main()
