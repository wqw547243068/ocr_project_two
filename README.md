# ocr_project

OCR 项目, 实现多文件类型、多语种的离线OCR检测功能


## 整体结构

整个项目分为
- (1) 前端代码: `ocr-ui` 目录
- (2) 后端代码: `backend` 目录
- 数据目录:
  - `cache_file` 用户上传文件缓存目录


## 前端


技术栈
- `Vite` + `React` + `TypeScript`

修改文件
- `vite.config.ts` 里 target处写后端接口 http：//ip +port
- `util/uploadfile.tsx` 68和71行改为 /api/oc

运行
- 先确保后端服务已启动

```sh
# 根目录, 删除 \node_modules 目录（如果存在）
npm install # 安装 node.js 工具包
npm run dev # 启动 Web UI 服务
```

详见[文档](ocr-ui/README.md)

## 后端

flask 构建的Python服务
- word 文档: 直接解析
- pdf 文档: 直接解析
- 图片文件: OCR 分别处理

启动后端服务

```sh
cd backend
python flask_web.py &>log.txt &
```



## 其它

