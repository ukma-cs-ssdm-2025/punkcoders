import Header from '../../Common.jsx';
import { useNavigate } from 'react-router-dom';

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div>
        <Header />
        <section className="menu-section">
        <h1>❓Page not found</h1>
        <p>We couldn't find whatever you were trying to view.</p>
        <button onClick={() => navigate(-1)}>Go Back</button>
        &nbsp;&nbsp;&nbsp;
        <button onClick={() => navigate('/')}>Go Home</button>
        </section>
    </div>
  );
};

export default NotFound;