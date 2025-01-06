import { Button, Message, Modal, Radio, Steps, Image, Tabs } from '@arco-design/web-react';
import UploadTpl from '../utils/uploadFile';
import { useEffect, useRef, useState } from 'react';
import { useLocation } from 'react-router';
import UEditorComponent from '../component/UEditorComponent'
import Markdown from 'react-markdown';
import {marked} from 'marked';

//const [result, setResult] = useState('')
// const result = `[null]`

const RadioGroup = Radio.Group
const Step = Steps.Step;
const TabPane = Tabs.TabPane;
const Step3 = (props) => {
  const editorRef = useRef(null);
  const [activeTab, setActiveTab] = useState('1')
  //  { props.children }
  console.log()
  return (<>
    <Tabs activeTab={activeTab} onChange={(key) => setActiveTab(key)}>
      <TabPane key='1' title='原始文件'>
       ${marked(result, { sanitize: true })}
       
      </TabPane>
      <TabPane key='2' title='在线调试'>
        <UEditorComponent id="ooooo" value={`<div style="text-align: left">${marked(result, { sanitize: true })}</div>`} onChange={() => {}} />
      </TabPane>
    </Tabs>
  </>)
}


export default function FileUpload(props: any) {
  const [step, setStep] = useState(1)
  const [visible, setVisible] = useState(false)
  const [value, setValue] = useState(0)
  const [imageSrc, setImageSrc] = useState('')
  const [tips, setTips] = useState<any>()
  const [result, setResult] = useState('')
  const [pdfFile, setPdfFile] = useState(null);  // 存储上传的 PDF 文件
  const [fileType, setFileType] = useState('');  // 存储上传的 PDF 文件
  const [pdfDoc, setPdfDoc] = useState(null);    // 存储加载后的 PDF 文档对象
  const [numPages, setNumPages] = useState(null); // PDF 的总页数
  const [canvases, setCanvases] = useState([]);   // 存储渲染的 canvas 元素
  const [rawfile, setRawfile] = useState('原始文件/预览图')
  const loc = useLocation()
  const doClick = () => {
    const dom = document.querySelector('.upload-tpl') as any;
    dom.querySelector('input[type="file"]').click()
  }

  function getPdf(file: any) {
    const reader = new FileReader();
    reader.onload = async function(e: any) {
      const pdfData = e.target.result;
      const typedArray = new Uint8Array(e.target.result);
      // 使用 PDF.js 加载 PDF 文件
      console.log('pdfcontainer----', document.getElementById('pdfContainer'))
      pdfjsLib.getDocument(typedArray).promise.then(function _getPdf(pdf:any) {
        // 获取 PDF 文件的总页数
        setPdfDoc(pdf);
        setNumPages(pdf.numPages)
      });      
      
    };

    file && reader.readAsArrayBuffer(file); // 以二进制流的方式读取 PDF 文件
  }

   // 渲染所有页面
   useEffect(() => {
    if (pdfDoc && numPages) {
      const renderPages = async () => {
        const newCanvases = [];
        for (let pageNum = 1; pageNum <= numPages; pageNum++) {
          const canvas = await renderPage(pageNum);
          newCanvases.push(canvas);
        }
        setCanvases(newCanvases as any);  // 更新 canvases 状态
      };

      renderPages();  // 渲染所有页面
    }
  }, [pdfDoc, numPages]);  // 当 PDF 文档或页数发生变化时触发渲染

  // 渲染页面到 canvas
  const renderPage = (pageNum: number) => {
    return new Promise((resolve) => {
      pdfDoc.getPage(pageNum).then((page: any) => {
        const viewport = page.getViewport({ scale: 1 });
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');

        canvas.width = viewport.width;
        canvas.height = viewport.height;

        // 渲染页面到 canvas
        page.render({
          canvasContext: context,
          viewport: viewport,
        }).promise.then(() => {
          resolve(canvas);  // 渲染完成后返回 canvas
        });
      });
    });
  };
  useEffect(() => {
    getPdf(pdfFile)
  }, [pdfFile])

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
        fileCb={(file: any) => {
          const type = file.type;
          if (type.includes('image/')) {
            setFileType('img');
            // 前端展示上传原始图片
            // const reader = new FileReader();
            // reader.onload = function (e: any) {
            //   setImageSrc(e.target.result);
              
            // }
            // reader.readAsDataURL(file); 
          } else if (file.type === 'application/pdf') {
            setFileType('pdf');
            setPdfFile(file);
          } 
        }}
        cback={(status: string, res: any) => {
          if (status === 'end') {
            setStep(3)
            if (res.status > 0) {
              console.log(res.data.content);
              setResult(res.data.content.join('\n'));
              setRawfile(res.req.file_name);
              if (res.data.merge_image) {
                setImageSrc(res.data.merge_image)
              }
            } else {
              setResult(res.msg || '识别失败，请检查您的文件后重新上传!');
              setRawfile(res.req.file_name || '原始文件/预览图');
            }
          } else if (status === 'error'){
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
      <Step3>
        <div id="pdfContainer" style={{flex: '1 1 50%', border: '1px solid #ccc', borderRadius: 4, height: 500, alignContent: 'center', overflow: 'scroll'}}>
          【预览】
          <div dangerouslySetInnerHTML={{ __html: rawfile }}></div>
          {fileType === 'pdf' && pdfFile ? canvases.map((canvas:any, index) => (
            <div key={index}>
              <canvas width={canvas.width} height={canvas.height} ref={(el) => el && (el.replaceWith(canvas))} />
            </div>
          )) : ''}
          {fileType === 'img' && imageSrc &&  <div style={{height: '100%', overflow: 'scroll'}}>
          <Image
            src={imageSrc}
            alt='原始图片'
          /></div>}
        </div>
      </Step3>
      {/* <div style={{display: 'flex', gap: 20}}>
        
        <div style={{flex: '1 1 50%', border: '1px solid #ccc', textAlign:'left', borderRadius: 4, height: 500,  color: '#165dff', overflowY: 'scroll'}}>
          
        <pre>{result}</pre>
          
        </div>
      </div> */}
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