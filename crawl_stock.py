import json

import requests

def get_stock_response(stock_code, start_date, end_date):
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://q.stock.sohu.com/cn/600919/lshq.shtml",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }
    url = "https://q.stock.sohu.com/hisHq"
    params = {
        "code": stock_code,
        "start": start_date,
        "end": end_date,
        "stat": "1",
        "order": "D",
        "period": "d",
        "callback": "historySearchHandler",
        "rt": "jsonp",
        "r": "0.7175042945435491",
        "0.17950639319396788": ""
    }
    response = requests.get(url, headers=headers, params=params)
    return response.text

def format_stock_data(stock_data):
    # Remove the callback wrapper from the response
    start_idx = stock_data.find('(')
    end_idx = stock_data.rfind(')')
    json_str = stock_data[start_idx+1:end_idx]

    data_json = json.loads(json_str)
    print(data_json)

    response_status = data_json[0]["status"]
    if str(response_status) != "0":
        print("数据获取失败: " + response_status)
        return None

    stock_info = data_json[0]["hq"]

    data_map = {}
    for item in stock_info:
        data_map[item[0]] = item[1:]
    return data_map