import Header from '../../Common.jsx';
import { useNavigate } from 'react-router-dom';

const Unauthorized = () => {
  const navigate = useNavigate();

  return (
    <div>
        <Header />
        <section className="menu-section">
        <h1>🚫 Access Denied</h1>
        <p>You do not have permission to view this page.</p>
        <button onClick={() => navigate(-1)}>Go Back</button>
        &nbsp;&nbsp;&nbsp;
        <button onClick={() => navigate('/')}>Go Home</button>
        </section>
    </div>
  );
};

export default Unauthorized;