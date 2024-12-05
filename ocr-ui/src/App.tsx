import { Outlet } from 'react-router';
import './App.css'

function App() {

  return (
    <div style={{ width: '100%', height: '100%',border: '1px solid #e5e6eb', borderRadius: '8px', padding: '8px', color: '#1d2129'}}>
      <Outlet />
    </div>
  )
}

export default App
