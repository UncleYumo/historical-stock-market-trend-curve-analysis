#!/bin/bash
# 生产环境启动脚本

# 检查环境变量文件
if [ -f ".env.prod" ]; then
    echo "使用生产环境配置..."
    export $(cat .env.prod | xargs)
else
    echo "未找到.env.prod文件，使用默认配置..."
fi

# 启动应用
python dashboard.py