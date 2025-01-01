import { Button, Message, Modal, Radio, Steps, Image, Tabs } from '@arco-design/web-react';
import UploadTpl from '../utils/uploadFile';
import { useEffect, useRef, useState } from 'react';
import { useLocation } from 'react-router';
import UEditorComponent from '../component/UEditorComponent'
import Markdown from 'react-markdown';
import {marked} from 'marked';
const mdText = `
# 中华人民共和国兵役法

> 1984年5月31日第六届全国人民代表大会第二次会议通过　
> 根据1998年12月29日第九届全国人民代表大会常务委员会第六次会议《关于修改〈中华人民共和国兵役法〉的决定》第一次修正　
> 根据2009年8月27日第十一届全国人民代表大会常务委员会第十次会议《关于修改部分法律的决定》第二次修正　
> 根据2011年10月29日第十一届全国人民代表大会常务委员会第二十三次会议《关于修改〈中华人民共和国兵役法〉的决定》第三次修正　2021年8月20日第十三届全国人民代表大会常务委员会第三十次会议修订

目　　录
- 第一章　总　　则
- 第二章　兵役登记
- 第三章　平时征集
- 第四章　士兵的现役和预备役
- 第五章　军官的现役和预备役
- 第六章　军队院校从青年学生中招收的学员
- 第七章　战时兵员动员
- 第八章　服役待遇和抚恤优待
- 第九章　退役军人的安置
- 第十章　法律责任
- 第十一章　附　　则

## 第一章　总　　则

- 第一条　为了规范和加强国家兵役工作，保证公民依法服兵役，保障军队兵员补充和储备，建设巩固国防和强大军队，根据宪法，制定本法。
- 第二条　保卫祖国、抵抗侵略是中华人民共和国每一个公民的神圣职责。
- 第三条　中华人民共和国实行以志愿兵役为主体的志愿兵役与义务兵役相结合的兵役制度。
- 第四条　兵役工作坚持中国共产党的领导，贯彻习近平强军思想，贯彻新时代军事战略方针，坚持与国家经济社会发展相协调，坚持与国防和军队建设相适应，遵循服从国防需要、聚焦备战打仗、彰显服役光荣、体现权利和义务一致的原则。
- 第五条　中华人民共和国公民，不分民族、种族、职业、家庭出身、宗教信仰和教育程度，都有义务依照本法的规定服兵役。有严重生理缺陷或者严重残疾不适合服兵役的公民，免服兵役。依照法律被剥夺政治权利的公民，不得服兵役。
- 第六条　兵役分为现役和预备役。在中国人民解放军服现役的称军人；预编到现役部队或者编入预备役部队服预备役的，称预备役人员。
- 第七条　军人和预备役人员，必须遵守宪法和法律，履行公民的义务，同时享有公民的权利；由于服兵役而产生的权利和义务，由本法和其他相关法律法规规定。
- 第八条　军人必须遵守军队的条令和条例，忠于职守，随时为保卫祖国而战斗。
  - 预备役人员必须按照规定参加军事训练、担负战备勤务、执行非战争军事行动任务，随时准备应召参战，保卫祖国。
  - 军人和预备役人员入役时应当依法进行服役宣誓。
- 第九条　全国的兵役工作，在国务院、中央军事委员会领导下，由国防部负责。
  - 省军区(卫戍区、警备区)、军分区(警备区)和县、自治县、不设区的市、市辖区的人民武装部，兼各该级人民政府的兵役机关，在上级军事机关和同级人民政府领导下，负责办理本行政区域的兵役工作。
  - 机关、团体、企业事业组织和乡、民族乡、镇的人民政府，依照本法的规定完成兵役工作任务。兵役工作业务，在设有人民武装部的单位，由人民武装部办理；不设人民武装部的单位，确定一个部门办理。普通高等学校应当有负责兵役工作的机构。
- 第十条　县级以上地方人民政府兵役机关应当会同相关部门，加强对本行政区域内兵役工作的组织协调和监督检查。
  - 县级以上地方人民政府和同级军事机关应当将兵役工作情况作为拥军优属、拥政爱民评比和有关单位及其负责人考核评价的内容。
- 第十一条　国家加强兵役工作信息化建设，采取有效措施实现有关部门之间信息共享，推进兵役信息收集、处理、传输、存储等技术的现代化，为提高兵役工作质量效益提供支持。
  - 兵役工作有关部门及其工作人员应当对收集的个人信息严格保密，不得泄露或者向他人非法提供。
- 第十二条　国家采取措施，加强兵役宣传教育，增强公民依法服兵役意识，营造服役光荣的良好社会氛围。
- 第十三条　军人和预备役人员建立功勋的，按照国家和军队关于功勋荣誉表彰的规定予以褒奖。
  - 组织和个人在兵役工作中作出突出贡献的，按照国家和军队有关规定予以表彰和奖励。

## 第二章　兵役登记

- 第十四条　国家实行兵役登记制度。兵役登记包括初次兵役登记和预备役登记。

## 第十一章　附　　则

- 第六十四条　本法适用于中国人民武装警察部队。
- 第六十五条　本法自2021年10月1日起施行。
`
const RadioGroup = Radio.Group
const Step = Steps.Step;
const TabPane = Tabs.TabPane;
const Step3 = (props) => {
  const editorRef = useRef(null);
  const [activeTab, setActiveTab] = useState('1')
  console.log()
  return (<>
    <Tabs activeTab={activeTab} onChange={(key) => setActiveTab(key)}>
      <TabPane key='1' title='原始文件'>
        { props.children }
      </TabPane>
      <TabPane key='2' title='在线调试'>
        <UEditorComponent id="ooooo" value={`<div style="text-align: center">${marked(mdText, { sanitize: true })}</div>`} onChange={() => {}} />
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
          {rawfile}
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