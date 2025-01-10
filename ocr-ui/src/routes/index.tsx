/*
 * @Author: weijingjing 1838352147@qq.com
 * @Date: 2025-01-09 20:55:30
 * @LastEditors: weijingjing 1838352147@qq.com
 * @LastEditTime: 2025-01-09 21:00:12
 * @FilePath: /ocr-project/ocr_project_two/ocr-ui/src/routes/index.tsx
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */


import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import App from "../App";
import Error from "../pages/Error";
import FileUpload from "../pages/FileUpload";
import OcrPage from "../pages/OcrPage";

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/',
        element: <OcrPage />,
      },
      {
        path: '/ocr',
        element: <FileUpload title="OCR识别" />,
      },
      {
        path: '/excel',
        element: <FileUpload title="表格识别" />,
      },
      {
        path: '/math',
        element: <FileUpload title="公式识别" />,
      },
      {
        path: '/img',
        element: <FileUpload title="图片识别" />,
      },
      {
        path: '/word',
        element: <FileUpload title="版面分析" />,
      },
      {
        path: '/revert',
        element: <FileUpload title="版面还原" />,
      },
      {
        path: '/paragraph',
        element: <FileUpload title="段落还原" />,
      },
      {
        path: '/pdf-to-word',
        element: <FileUpload title="PDF转Word" />,
      },
      {
        path: '/keywords',
        element: <FileUpload title="文件整编" />,
      },
      {
        path: '/keywords-remove',
        element: <FileUpload title="关键内容移除" />,
      },
      {
        path: '/standard',
        element: <FileUpload title="标准化" />,
      },
      {
        path: '/slice',
        element: <FileUpload title="章节切分" />,
      },
    ],
    ErrorBoundary: Error,
  },
]);

export default function Routes() {
  return <RouterProvider router={router} />
}