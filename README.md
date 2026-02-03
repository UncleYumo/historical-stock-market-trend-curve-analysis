# 股票价格交互式分析仪表盘

基于Python Flask的单体Web应用，提供中英文界面和股票数据分析功能。

## 功能特性

- 股票历史数据分析
- 多语言支持（中文/英文）
- 交互式图表展示
- 数据表格显示
- CSV导出功能
- 响应式设计

## 环境变量配置

本项目支持多种环境变量配置文件，优先级如下：
1. `.env.local` - 本地开发配置
2. `.env.prod` - 生产环境配置  
3. `.env` - 默认配置

### 配置选项

- `PORT`: 应用端口（默认: 5000）
- `HOST`: 主机地址（默认: 127.0.0.1）
- `DEBUG`: 调试模式（默认: True）

## 安装依赖

```bash
pip install -r requirements.txt
```

或者单独安装：

```bash
pip install flask plotly pandas requests python-dotenv
```

## 运行方式

### 开发模式

```bash
python dashboard.py
```

### 生产模式

#### 方法一：使用Gunicorn（推荐）

1. 安装Gunicorn：
```bash
pip install gunicorn
```

2. 使用生产环境配置运行：
```bash
# 设置生产环境变量
cp .env.prod .env  # 或者确保设置了生产环境变量

# 启动服务
gunicorn --workers 4 --bind 0.0.0.0:8000 --timeout 120 dashboard:app
```

#### 方法二：直接运行（适用于简单部署）

1. 确保环境变量文件配置正确（.env.prod）
2. 直接运行：
```bash
python dashboard.py
```

## 部署建议

### 生产环境部署

1. **使用专用WSGI服务器**（如Gunicorn）：
   - 提供更好的性能和稳定性
   - 支持多进程处理并发请求

2. **反向代理设置**（如Nginx）：
   - 处理静态文件
   - 提供SSL/TLS支持
   - 负载均衡

3. **安全考虑**：
   - 设置DEBUG=False
   - 使用HTTPS
   - 配置适当的安全头

4. **环境变量**：
   - 使用`.env.prod`配置生产环境参数
   - 不要在代码中硬编码敏感信息

### Docker部署（可选）

创建Dockerfile：

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "--timeout", "120", "dashboard:app"]
```

构建并运行：

```bash
docker build -t stock-dashboard .
docker run -p 8000:8000 --env-file .env.prod stock-dashboard
```

## 访问应用

- 开发模式：`http://127.0.0.1:5000`
- 生产模式：`http://your-server-ip:8000`

## 文件结构

```
├── dashboard.py          # 主应用文件
├── app.py               # 原始应用文件（已备份）
├── crawl_stock.py       # 股票数据爬取模块
├── templates/index.html # 前端模板
├── .env                 # 默认环境变量
├── .env.local           # 本地开发环境变量
├── .env.prod            # 生产环境变量
├── requirements.txt     # 依赖包列表
└── README.md           # 说明文档
```

## 环境变量文件说明

- `.env`：默认配置，适用于大多数情况
- `.env.local`：本地开发专用配置，不会被提交到版本控制
- `.env.prod`：生产环境配置，包含生产环境特定设置

系统会按照优先级自动加载合适的配置文件。