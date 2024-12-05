import { Button, Message, Modal, Radio, Steps } from '@arco-design/web-react';
import UploadTpl from '../utils/uploadFile';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
const RadioGroup = Radio.Group
const Step = Steps.Step;

export default function FileUpload() {
  const [step, setStep] = useState(1)
  const [visible, setVisible] = useState(false)
  const [value, setValue] = useState(0)
  const [result, setResult] = useState('')
  const [rawfile, setRawfile] = useState('')
  const navigate = useNavigate()
  const doClick = () => {
    const dom = document.querySelector('.upload-tpl') as any;
    dom.querySelector('input[type="file"]').click()
    setTimeout(() => {
      setStep(2)
    }, 3000)
  }

  const goBack = () => {
    navigate('/')
  }

  useEffect(() => {
    if (step === 2) {
      setTimeout(() => {
        setStep(3)
      }, 3000)
    }
  }, [step])

  return <div style={{textAlign: 'center'}}>
    <div className='go-back' style={{textAlign: 'left'}} onClick={() => goBack()}>
      <img style={{cursor: 'pointer', width: 16}} src="/back.png" alt="upload" onClick={() => doClick()} /><span style={{cursor: 'pointer'}}>返回</span>
    </div>
    <h1>OCR识别</h1>
    <h2>高精度识别</h2>
    <div className='step' style={{marginBottom: 16, height: 60,cursor: 'pointer' }}>
      <Steps current={step} onChange={(step) => {setStep(step)}} style={{  margin: '0 auto', maxWidth: 780, }}>
        <Step title='上传文件' />
        <Step title='在线识别' />
        <Step title='导出结果' />
      </Steps>
    </div>
    {/* <Button
      type="primary"
      loading={uploading}
      onClick={() => {
      uploadAjax()
    }} icon={<IconUpload />}>点击上传</Button> */}

    {step === 1 && <div className='upload-area'>
      <div><img style={{cursor: 'pointer'}} src="/upload.png" alt="upload" onClick={() => doClick()} /></div>
      <UploadTpl
        cback={(status: string, res:any) => {
          // setUploading(true)
          // setStep(2)
          if (status === 'end') {
            // setUploading(false)
            // console.log(res.status, 123)
            setResult(res.data.content.join('\n'))
            setRawfile(res.req.file_name)
          }
        }}
      />

      <h3>点击此处上传文件/拖拽文件到此处上传</h3>
      <p>支持上传doc、docx、pdf、png、jpg、jpeg格式</p>
      <p>支持识别中文、英文、日语、法语、德语</p>
      <p>支持印刷体、手写体</p>
    </div>}
    {step === 2 && <div className='upload-area'>
      <div><img style={{cursor: 'pointer'}} src="/pending.png" alt="loading..." /></div>
      
      <h3>努力识别中，请稍后.....</h3>
    </div>}
    {step === 3 && <div>
      <div style={{display: 'flex', gap: 20}}>
        <div style={{flex: '1 1 50%', border: '1px solid #ccc', borderRadius: 4, height: 500, alignContent: 'center'}}>
          原始文件/预览图
          {rawfile}
        </div>
        <div style={{flex: '1 1 50%', border: '1px solid #ccc', borderRadius: 4, height: 500, alignContent: 'center', color: '#165dff'}}>
          文字识别结果
          {result}
        </div>
      </div>
      <div style={{display: 'flex', justifyContent: 'end', marginTop: 10}}>
        <Button type="primary" style={{visibility: 'hidden'}}>导出</Button>
        <div style={{flexBasis: '100%'}}>
          <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer'}}>          
            <img onClick={() => setStep(1)} style={{ height: 28, marginRight: 8}} src="/reupload.png" alt="loading..." />
            <span onClick={() => setStep(1)} style={{fontSize: 16}}>重新上传</span>
          </div>
        </div>
        <Button type="primary" onClick={() => setVisible(true)}>导出</Button>
      </div>
    </div>}
    <div style={{padding: 20, textAlign: 'center'}}>
      我们尊重隐私权。在文件转换/识别后，它们将永远从我们的服务器删除
    </div>

    <Modal
      title="选择格式"
      visible={visible}
      onOk={() => {
        setVisible(false)
        setValue(0)
        Message.success('导出成功')
      }}
      onCancel={() => {
        setVisible(false)
        setValue(0)
      }}
    >
      <div>请选择导出格式</div>
      <div style={{marginTop: 16}}>
        <RadioGroup value={value} onChange={(val) => setValue(val)} options={[
          {
            label: 'TXT',
            value: 1,
          },
          {
            label: 'JSON',
            value: 2,
          },
          {
            label: 'Markdown',
            value: 3,
          },
          {
            label: 'Word',
            value: 4,
          },
        ]}>
          
        </RadioGroup>
      </div>
    </Modal>
  </div>
}