import { Button, Message, Modal, Radio, Steps } from '@arco-design/web-react';
import UploadTpl from '../utils/uploadFile';
import { useEffect, useState } from 'react';
import { useLocation } from 'react-router';
const RadioGroup = Radio.Group
const Step = Steps.Step;

export default function FileUpload(props: any) {
  const [step, setStep] = useState(1)
  const [visible, setVisible] = useState(false)
  const [value, setValue] = useState(0)
  const [imageSrc, setImageSrc] = useState('')
  const [tips, setTips] = useState<any>()
  const [result, setResult] = useState('')
  const [rawfile, setRawfile] = useState('原始文件/预览图')
  const loc = useLocation()
  const doClick = () => {
    const dom = document.querySelector('.upload-tpl') as any;
    dom.querySelector('input[type="file"]').click()
  }

  useEffect(() => {
    if (loc.pathname === '/revert') {
      setTips(<div><p>支持上传pdf、doc、docx、html格式</p><p>支持识别并修正错误拆分的段落合并、未正确分段的部分拆分</p></div>)
    } else if (loc.pathname === '/ocr') {
      setTips(<div>
      <p>支持上传doc、docx、pdf、png、jpg、jpeg格式</p>
      <p>支持识别中文、英文、日语、法语、德语</p>
      <p>支持印刷体、手写体</p>
      </div>)
    } else if (loc.pathname === '/excel') {
      setTips(<div>
        <p>支持上传xls、xlsx格式</p>
        <p>支持识别中文、英文及多语种混杂</p>
        <p>支持印刷体、手写体</p>
        </div>)
    } else if (loc.pathname === '/math') {
      setTips(<div>
        <p>支持上传doc、docx、pdf、png、jpg、jpeg格式</p>
        <p>支持识别行间、行内公式</p>
        </div>)
    } else if (loc.pathname === '/img') {
      setTips('支持上传doc、docx、pdf、png、jpg、jpeg格式')
    } else if (loc.pathname === '/word') {
      setTips('支持识别正文、参考文献、数学公式、目录、页眉、页脚、插图说明、表格及其题注')
    } else if (loc.pathname === '/slice') {
      setTips(<div>支持上传doc、docx格式
        <p>支持按照目录进行章节切分</p></div>)
    } else if (loc.pathname === '/standard') {
      setTips(<p>支持上传doc、docx格式</p>)
    }
  }, [loc.pathname])

  return <div style={{textAlign: 'center'}}>
    <h1>{props.title}</h1>
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

    {step === 1 && <div className='upload-area' style={{margin: '30px 0'}}>
      <div><img style={{cursor: 'pointer'}} src="/upload.png" alt="upload" onClick={() => doClick()} /></div>
      <UploadTpl
        cback={(status: string, res: any) => {
          if (status === 'end') { // 上传成功
            setStep(3)
            if (res.status > 0) { // ocr成功
              setResult(res.data.content.join('\n'));
              setRawfile(res.req.file_name);
              if (res.data.merge_image) {
                setImageSrc(res.data.merge_image)
              }
            } else { // ocr失败
              setResult(res.msg || '识别失败，请检查您的文件后重新上传!');
              setRawfile(res.req.file_name || '原始文件/预览图');
            }
          } else if (status === 'error'){ // 上传失败
            setStep(3)
            setResult('识别失败，请检查您的文件后重新上传!');
            setRawfile('原始文件/预览图');
          } else {
            setStep(2)
          }
        }}
      />

      <h3>点击此处上传文件/拖拽文件到此处上传</h3>
      {tips}
    </div>}
    {step === 2 && <div className='upload-area'>
      <div><img style={{cursor: 'pointer'}} src="/pending.png" alt="loading..." /></div>
      
      <h3>努力识别中，请稍后.....</h3>
    </div>}
    {step === 3 && <div>
      <div style={{display: 'flex', gap: 20}}>
        <div style={{flex: '1 1 50%', border: '1px solid #ccc', borderRadius: 4, height: 500, alignContent: 'center', overflow: 'hidden'}}>
          {rawfile}
          {imageSrc &&  <div style={{height: 500, width: '100%', overflow: 'scroll'}}><img src={imageSrc} ></img></div>}
        </div>
        <div style={{flex: '1 1 50%', border: '1px solid #ccc', borderRadius: 4, height: 500,  fontSize: '15px', color: '#21618c', overflowY: 'scroll', textAlign:'left'}}>
          <pre>{result}</pre>
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