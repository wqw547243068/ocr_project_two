import { useNavigate } from 'react-router';
const data = [
  {
    key: 'a',
    title: '文档格式助手',
    list: [
      {
        key: '/word',
        icon: '/1.png',
        text: '版面分析',
      },
      {
        key: '/revert',
        icon: '/2.png',
        text: '版面还原',
      },
      {
        key: '/paragraph',
        icon: '/3.png',
        text: '段落还原',
      },
      {
        key: '/pdf-to-word',
        icon: '/4.png',
        text: 'PDF转Word',
      },
    ]
  },
  {
    key: 'b',
    title: '高精度识别',
    list: [
      {
        icon: '/5.png',
        key: 'ocr',
        text: 'OCR识别',
      },
      {
        key: '/excel',
        icon: '/6.png',
        text: '表格识别',
      },
      {
        key: '/math',
        icon: '/7.png',
        text: '公式识别',
      },
      {
        key: '/img',
        icon: '/8.png',
        text: '图片识别',
      },
    ]
  },
  {
    key: 'c',
    title: '文档内容助手',
    list: [
      {
        key: '/keywords',
        icon: '/9.png',
        text: '文件整编',
      },
      {
        key: '/keywords-remove',
        icon: '/10.png',
        text: '关键内容移除',
      },
      {
        key: '/standard',
        icon: '/11.png',
        text: '标准化',
      },
      {
        key: '/slice',
        icon: '/12.png',
        text: '章节切分',
      },
    ]
  }
]


const OcrPage = () => {
  const navigate = useNavigate()
  const doClick = (key: any) => {
    if (key === 'ocr') {
      navigate('/ocr')
    } else {
      navigate(key)
    }
  }
  
  return (
    <div style={{padding: 30}}>
      {
        data.map(item => {
          return <div key={item.key} style={{marginBottom: 60, textAlign: 'left'}}>
            <div style={{fontSize: 28, fontWeight: 500, marginBottom: 12}}>{item.title}</div>
            <div style={{display: 'flex', justifyContent: 'space-between'}}>
              {
                item.list.map(obj => {
                  return <div key={obj.text} style={{display: 'flex', alignItems: 'center', cursor: 'pointer'}} onClick={() => doClick(obj.key)}>
                    <img style={{width: 60}} src={obj.icon} alt={obj.text} />
                    <span>{obj.text}</span>
                  </div>
                })
              }
            </div>
          </div>
        })
      }
    </div>
  );
};

export default OcrPage;
