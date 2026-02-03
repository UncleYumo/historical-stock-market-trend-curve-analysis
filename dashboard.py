"""
股票价格交互式分析仪表盘
基于Python Flask的单体Web应用，提供中英文界面和股票数据分析功能
"""

from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
from crawl_stock import get_stock_response, format_stock_data
import plotly
import plotly.graph_objs as go
from datetime import datetime


class StockDashboard:
    """股票仪表盘主类，管理应用状态和业务逻辑"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.stock_data_map = {
            "code": "",
            "start_date": "",
            "end_date": "",
            "data": {},
            "cumulative_data": {},
            "current_lang": "zh"
        }
        self.translations = self._init_translations()
        self._setup_routes()
    
    def _init_translations(self):
        """初始化多语言翻译字典"""
        return {
            'en': {
                'title': 'Stock Price Interactive Analysis Dashboard',
                'stock_code': 'Stock Code',
                'start_date': 'Start Date',
                'end_date': 'End Date',
                'interval': 'Interval',
                'daily': 'Daily',
                'weekly': 'Weekly',
                'monthly': 'Monthly',
                'submit': 'Submit',
                'chinese': 'Chinese',
                'english': 'English',
                'date': 'Date',
                'open': 'Open',
                'close': 'Close',
                'high': 'High',
                'low': 'Low',
                'volume': 'Volume',
                'amount': 'Amount',
                'change_amount': 'Change Amount',
                'change_percent': 'Change Percent',
                'turnover_rate': 'Turnover Rate',
                'stock_data': 'Stock Data',
                'trend_chart': 'Trend Chart',
                'loading': 'Loading...',
                'select_language': 'Select Language',
                'cumulative_data': 'Cumulative Data',
                'export_csv': 'Export CSV',
                'refresh_data': 'Refresh Data',
                'stock_name': 'Stock Name',
                'latest_price': 'Latest Price',
                'price_change': 'Price Change',
                'price_change_percent': 'Price Change %',
                'volume_info': 'Volume Info',
                'market_cap': 'Market Cap',
                'pe_ratio': 'P/E Ratio',
                'about': 'About',
                'instructions': 'Instructions',
                'contact': 'Contact'
            },
            'zh': {
                'title': '股票价格交互式分析仪表盘',
                'stock_code': '股票代码',
                'start_date': '开始日期',
                'end_date': '结束日期',
                'interval': '间隔',
                'daily': '日',
                'weekly': '周',
                'monthly': '月',
                'submit': '提交',
                'chinese': '中文',
                'english': '英文',
                'date': '日期',
                'open': '开盘',
                'close': '收盘',
                'high': '最高',
                'low': '最低',
                'volume': '成交量',
                'amount': '成交金额',
                'change_amount': '涨跌额',
                'change_percent': '涨跌幅',
                'turnover_rate': '换手率',
                'stock_data': '股票数据',
                'trend_chart': '趋势图',
                'loading': '加载中...',
                'select_language': '选择语言',
                'cumulative_data': '累计数据',
                'export_csv': '导出CSV',
                'refresh_data': '刷新数据',
                'stock_name': '股票名称',
                'latest_price': '最新价',
                'price_change': '涨跌额',
                'price_change_percent': '涨跌幅%',
                'volume_info': '成交量信息',
                'market_cap': '市值',
                'pe_ratio': '市盈率',
                'about': '关于',
                'instructions': '使用说明',
                'contact': '联系'
            }
        }
    
    def _setup_routes(self):
        """设置路由"""
        self.app.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.app.add_url_rule('/fetch_data', 'fetch_data', self.fetch_data, methods=['POST'])
        self.app.add_url_rule('/get_chart_data', 'get_chart_data', self.get_chart_data, methods=['GET'])
        self.app.add_url_rule('/export_csv', 'export_csv', self.export_csv, methods=['POST'])
    
    def index(self):
        """主页路由"""
        lang = request.args.get('lang', 'zh')
        self.stock_data_map["current_lang"] = lang
        t = self.translations[lang]
        
        # 提供默认值
        default_code = self.stock_data_map["code"] or "cn_600919"
        default_start = self.stock_data_map["start_date"] or "20250101"
        default_end = self.stock_data_map["end_date"] or "20260203"
        
        return render_template('index.html', t=t, lang=lang, 
                              default_code=default_code, 
                              default_start=default_start, 
                              default_end=default_end)
    
    def fetch_data(self):
        """获取股票数据API"""
        data = request.json
        stock_code = data.get('stock_code', 'cn_600919')
        start_date = data.get('start_date', '20250101')
        end_date = data.get('end_date', '20260203')
        interval = data.get('interval', 'd')  # d: daily, w: weekly, m: monthly
        
        # 更新全局变量
        self.stock_data_map["code"] = stock_code
        self.stock_data_map["start_date"] = start_date
        self.stock_data_map["end_date"] = end_date
        
        try:
            # 设置请求头
            headers = {
                "accept": "*/*",
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "referer": f"https://q.stock.sohu.com/cn/{stock_code.replace('cn_', '')}/lshq.shtml",
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
                "period": interval,  # 这里设置间隔类型
                "callback": "historySearchHandler",
                "rt": "jsonp",
                "r": "0.7175042945435491",
                "0.17950639319396788": ""
            }
            import requests
            response = requests.get(url, headers=headers, params=params)
            raw_data = response.text
            
            formatted_data = format_stock_data(raw_data)
            
            if formatted_data:
                self.stock_data_map["data"] = formatted_data
                
                # 提取累计数据 (从原始响应中提取)
                start_idx = raw_data.find('(')
                end_idx = raw_data.rfind(')')
                json_str = raw_data[start_idx+1:end_idx]
                data_json = json.loads(json_str)
                
                if len(data_json) > 0 and 'stat' in data_json[0]:
                    stat_info = data_json[0]['stat']
                    self.stock_data_map["cumulative_data"] = {
                        'period': stat_info[1] if len(stat_info) > 1 else '',
                        'change_amount': stat_info[2] if len(stat_info) > 2 else '',
                        'change_percent': stat_info[3] if len(stat_info) > 3 else '',
                        'lowest': stat_info[4] if len(stat_info) > 4 else '',
                        'highest': stat_info[5] if len(stat_info) > 5 else '',
                        'total_volume': stat_info[6] if len(stat_info) > 6 else '',
                        'total_amount': stat_info[7] if len(stat_info) > 7 else '',
                        'turnover_rate': stat_info[8] if len(stat_info) > 8 else ''
                    }
                else:
                    self.stock_data_map["cumulative_data"] = {}
                    
                return jsonify({
                    'success': True, 
                    'data': formatted_data,
                    'cumulative_data': self.stock_data_map["cumulative_data"],
                    'columns': ['date', 'open', 'close', 'change_amount', 'change_percent', 'low', 'high', 'volume', 'amount', 'turnover_rate'],
                    'code': stock_code,
                    'dates': list(formatted_data.keys()) if formatted_data else []
                })
            else:
                return jsonify({'success': False, 'error': 'Failed to fetch stock data'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    def get_chart_data(self):
        """获取图表数据API"""
        if not self.stock_data_map["data"]:
            return jsonify({'success': False, 'error': 'No data available'})
        
        # 准备图表数据
        dates = []
        opens = []
        closes = []
        highs = []
        lows = []
        
        for date, values in self.stock_data_map["data"].items():
            dates.append(date)
            opens.append(float(values[0]) if values[0] != '' and values[0] is not None else 0)
            closes.append(float(values[1]) if values[1] != '' and values[1] is not None else 0)
            # 根据数据格式，索引5是最高价，索引4是最低价
            highs.append(float(values[5]) if len(values) > 5 and values[5] != '' and values[5] is not None else 0)
            lows.append(float(values[4]) if len(values) > 4 and values[4] != '' and values[4] is not None else 0)
        
        # 创建蜡烛图
        candlestick_trace = go.Candlestick(
            x=dates,
            open=opens,
            high=highs,
            low=lows,
            close=closes,
            name='Price',
            increasing_line_color='red',
            decreasing_line_color='green'
        )
        
        # 添加收盘价线图
        close_trace = go.Scatter(
            x=dates,
            y=closes,
            mode='lines',
            name='Close Price',
            line=dict(color='blue', width=1),
            opacity=0.6
        )
        
        layout = go.Layout(
            title='Stock Price Trend',
            xaxis=dict(title='Date', rangeslider=dict(visible=False)),
            yaxis=dict(title='Price'),
            height=600,
            hovermode='x unified'
        )
        
        fig = go.Figure(data=[candlestick_trace, close_trace], layout=layout)
        
        # 转换为JSON
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return jsonify({'success': True, 'data': graphJSON})
    
    def export_csv(self):
        """导出数据为CSV格式"""
        import io
        import csv
        from flask import Response
        
        if not self.stock_data_map["data"]:
            return jsonify({'success': False, 'error': 'No data available'})
        
        # 准备CSV数据
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 写入表头
        writer.writerow(['Date', 'Open', 'Close', 'Change_Amount', 'Change_Percent', 'Low', 'High', 'Volume', 'Amount', 'Turnover_Rate'])
        
        # 写入数据
        for date, values in self.stock_data_map["data"].items():
            row = [date] + values
            writer.writerow(row)
        
        # 获取CSV内容
        csv_content = output.getvalue()
        output.close()
        
        # 返回CSV文件
        from flask import make_response
        response = make_response(csv_content)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=stock_data_{self.stock_data_map["code"]}.csv'
        
        return response
    
    def run(self, debug=True):
        """运行应用"""
        self.app.run(debug=debug)


if __name__ == '__main__':
    dashboard = StockDashboard()
    dashboard.run()