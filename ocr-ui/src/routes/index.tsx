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
        element: <FileUpload />,
      }
    ],
    ErrorBoundary: Error,
  },
]);

export default function Routes() {
  return <RouterProvider router={router} />
}