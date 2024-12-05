# ocr_project

OCR 项目


## 整体结构

整个项目分为
- 前端: UI
- 代码目录: orc_ui

## 前端

修改文件
- vite.config.ts 里 target处写后端接口 http：//ip +port
- util/uploadfile.tsx 68和71行改为/api/oc

运行

```sh
# 根目录执行
npm install
npm run dev
```


## 后端

flask 构建的Python服务
- word 文档: 直接解析
- pdf 文档: 直接解析
- 图片文件: OCR 分别处理


## 其它

