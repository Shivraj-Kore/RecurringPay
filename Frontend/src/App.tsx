import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import App from './App';
import HomePage from './pages/HomePage';

function AppRoutes() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/home" element={<HomePage />} />
      </Routes>
    </Router>
  );
}

export default AppRoutes;
