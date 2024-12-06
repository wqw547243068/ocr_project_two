import { useState } from 'react'
import { Upload, Message } from '@arco-design/web-react'

export const uploadAjax = () => {
  const dom:any = document.getElementById('upload-tpl')
  console.log('uploadAjax', dom.querySelector('input[type="file"]'))

  const evt = new MouseEvent('click', {
    bubbles: true,
    cancelable: true,
    view: window,
  })
  dom.querySelector('input[type="file"]').dispatchEvent(evt)
}

function UploadTpl(props: any) {
  const [fileList, setFileList] = useState([])
  return (
    <Upload
      drag
      style={{ display: 'none' }}
      className="upload-tpl"
      fileList={fileList}
      // limit={1}
      showUploadList={false}
      onChange={setFileList as any}
      customRequest={(option) => {
        const { onProgress, onError, onSuccess, file } = option as any;
        // const name = file?.name || 'file'
        props.cback()
        const xhr = new XMLHttpRequest()
        xhr.withCredentials = false
        if (xhr.upload) {
          xhr.upload.onprogress = function (event) {
            let percent
            if (event.total > 0) {
              percent = (event.loaded / event.total) * 100
            }

            onProgress(parseInt(percent as any, 10), event)
          }
        }

        xhr.onerror = function error(e) {
          onError(e)
        }

        xhr.onload = function onload() {
          if (xhr.status < 200 || xhr.status >= 300) {
            Message.error('解析失败')
            props.cback('error')
            return onError(xhr.responseText as any)
          }
          const res = JSON.parse(xhr.responseText)

          if (res.code === 0) {
            onSuccess(xhr.responseText, xhr)
            Message.success(res.msg || '上传成功')
          } else {
            Message.success(res.errmsg || '上传成功')
          }
          props.cback('end', res)
        }

        const formData = new FormData()
        formData.append('uploadFile', file)
        if (import.meta.env.DEV) {
          xhr.open('post', '/api/api_ocr', true)
        } else {
          xhr.open('post', '/api/api_ocr', true)
        }

        xhr.send(formData)
        return {
          abort() {
            xhr.abort()
          },
        }
      }}
    />
  )
}

export default UploadTpl
