import { Result, Button } from '@arco-design/web-react';
import { useNavigate } from 'react-router';

const Error = () => {
  const navigate = useNavigate()
  return (
    <div>
      <Result
        status='500'
        subTitle='This page isn’t working.'
        extra={<Button type='primary' onClick={() => navigate('/')}>Back</Button>}
      ></Result>
    </div>
  );
};

export default Error;
