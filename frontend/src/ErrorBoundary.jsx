import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Неперехоплена помилка в компоненті:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '2rem', textAlign: 'center' }}>
          <h2>Ой! Щось пішло не так.</h2>
          <p>Ми вже працюємо над виправленням. Спробуйте оновити сторінку.</p>
          <button onClick={() => this.setState({ hasError: false })}>
            Спробувати знову
          </button>
        </div>
      );
    }

    return this.props.children; 
  }
}

export default ErrorBoundary;