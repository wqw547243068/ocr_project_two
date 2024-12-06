import { Outlet, useNavigate } from 'react-router';
import './App.css'
import { Breadcrumb, Layout, Menu } from '@arco-design/web-react';
import Content from '@arco-design/web-react/es/Layout/content';
import Footer from '@arco-design/web-react/es/Layout/footer';
import Sider from '@arco-design/web-react/es/Layout/sider';
import SubMenu from '@arco-design/web-react/es/Menu/sub-menu';
const MenuItem = Menu.Item;
function App() {
  const navigate = useNavigate()
  const goBack = () => {
    navigate('/')
  }
  return (
    <div>
        <div style={{ paddingLeft: 20, background: '#165dff', height: '60px', paddingTop: '12px', fontSize: 25, textAlign: 'left', fontFamily: 'sans-serif' }}>文档数字化平台</div>
        <Layout style={{color: '#1d2129',height: 'calc(100vh - 60px)'}}>
          <Sider
            // collapsed={this.state.collapsed}
            // onCollapse={this.handleCollapsed}
            collapsible
            // trigger={this.state.collapsed ? <IconCaretRight /> : <IconCaretLeft />}
            breakpoint='xl'
          >
            <div className='logo' />
            <Menu
              defaultOpenKeys={['1']}
              defaultSelectedKeys={['0_1']}
              onClickMenuItem={(key: any) =>
                {
                  navigate(key)
                }
              }
              style={{ width: '100%', textAlign:'left' }}
            >
              <MenuItem key='/'>
                导航首页
              </MenuItem>
              <SubMenu
                key='1'
                title="文档识别助手"
              >
                <MenuItem key='/ocr'>OCR识别</MenuItem>
                <MenuItem key='/excel'>表格识别</MenuItem>
                <MenuItem key='/math'>公式识别</MenuItem>
                <MenuItem key='/img'>图片识别</MenuItem>
              </SubMenu>
              <SubMenu key='2' title='文档格式助手'>
                <MenuItem key='/word'>版面分析</MenuItem>
                <MenuItem key='/revert'>版面还原</MenuItem>
                <MenuItem key='/paragraph'>段落还原</MenuItem>
                <MenuItem key='/pdf-to-word'>PDF转Word</MenuItem>
              </SubMenu>
              <SubMenu key='3' title='文档内容助手'>
                <MenuItem key='/keywords'>关键内容识别</MenuItem>
                <MenuItem key='/keywords-remove'>关键内容移除</MenuItem>
                <MenuItem key='/standard'>标准化</MenuItem>
                <MenuItem key='/slice'>章节切分</MenuItem>
              </SubMenu>
            </Menu>
          </Sider>
          <Layout style={{ padding: '0 20px' }}>
            <Breadcrumb style={{ margin: '10px 0', textAlign: 'left', cursor: 'pointer' }}>
              <Breadcrumb.Item onClick={() => goBack()}>
              <img style={{cursor: 'pointer', width: 16, position: 'relative', top: '-1px'}} src="/back.png" alt="upload" />
                &nbsp;首页导航
              </Breadcrumb.Item>
              <Breadcrumb.Item>List</Breadcrumb.Item>
            </Breadcrumb>
            <Content>
              <div style={{border: '1px solid #e5e6eb', background: '#fff', borderRadius: '8px', padding: '8px'}}>
                <Outlet />
              </div>
            </Content>
            <Footer style={{minHeight: 50, maxHeight: 50, height: 50, alignContent: 'center', color: 'gray'}}>
              <img src="/footer.png" alt="tip" width={20} height={20} style={{verticalAlign: 'top', marginRight: 6}} />我们尊重隐私权。在文件转换/识别后，它们将永远从我们的服务器删除</Footer>
          </Layout>
        </Layout>
      </div>
  )
}

export default App
