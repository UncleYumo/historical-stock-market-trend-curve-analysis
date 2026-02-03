import pandas as pd
from matplotlib import pyplot as plt

from crawl_stock import get_stock_response, format_stock_data

stock_data_map = {
    "code": "",
    "start_date": "",
    "end_date": "",
    "data": {},
    "stock_trend_data_range": 50
}

def update_stock_data(code, start, end):
    stock_data_map["code"] = code
    stock_data_map["start_date"] = start
    stock_data_map["end_date"] = end

def fetch_stock_data():
    stock_data = get_stock_response(
        stock_data_map["code"],
        stock_data_map["start_date"],
        stock_data_map["end_date"]
    )
    stock_data_map["data"] = format_stock_data(stock_data)

def draw_chart():
    date_list = []
    opening_price_list = []
    closing_price_list = []
    data_map = dict(list(stock_data_map["data"].items())[:stock_data_map["stock_trend_data_range"]])
    for date, values in data_map.items():
        date_list.append(date)
        opening_price_list.append(float(values[0]))
        closing_price_list.append(float(values[1]))
    df = pd.DataFrame({
        "Date": date_list,
        "Opening Price": opening_price_list,
        "Closing Price": closing_price_list
    })
    df.set_index("Date", inplace=True)
    plt.figure(figsize=(1200, 200))  # 设置图表大小
    plt.title('Stock Opening and Closing Price Over Time')  # 图表标题
    plt.plot(df.index, df['Opening Price'], label='Opening Price')
    plt.plot(df.index, df['Closing Price'], label='Closing Price')
    plt.grid(True)  # 显示网格
    plt.xticks(rotation=45)  # 旋转x轴日期标签以适应图表
    plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
    plt.show()  # 展示图表

def main():
    update_stock_data("cn_600919", "20260110", "20260202")
    fetch_stock_data()
    draw_chart()

if __name__ == '__main__':
    main()