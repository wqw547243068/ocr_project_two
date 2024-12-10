:: windows bat 脚本

@echo off

SET "python=C:\Users\wqw\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.11"
SET "npm=E:\program_file\npm.cmd"

::date
::time

dir .

echo 检查日志目录

IF exist log (
  echo 日志目录已存在
) ELSE (
  echo 日志目录不存在,创建...
  md log
)

echo 启动后端程序

python backend/flask_web.py >> log\log_backend.txt

REM UNKNOWN: {"type":"Redirect","op":{"text":">","type":"great"},"file":{"text":"log_backend.txt","type":"Word"}}

echo 启动前端服务

cd ocr-ui

npm run dev >> log\log_foreend.txt

REM UNKNOWN: {"type":"Redirect","op":{"text":">","type":"great"},"file":{"text":"log_foreend.txt","type":"Word"}}
[ %?% EQU 0 ] && echo 项目启动完毕, 可以访问 Web || echo 项目启动失败

echo OCR程序启动完毕

pause