#!/bin/bash

# 环境变量
python="/usr/env/python311"
npm="/usr/bin/npm"

# 进入项目目录
# cd ocr_project
ls .
# log 目录
[ -d log ] || echo "日志目录已存在" && { echo "日志目录不存在,创建...";mkdir log; }

# 启动后端
$python flask_web.py &> log_backend.txt
# 启动前端
$npm run dev &>log_foreend.txt

[ $? -eq 0 ] && echo "项目启动完毕, 可以访问 Web" || echo "项目启动失败"