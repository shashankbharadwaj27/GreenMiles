import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/Landing";
import EVInput from "./pages/EVInput";
import HVInput from "./pages/HVInput";
import Results from "./pages/Results";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/results" element={<Results />} />
        <Route path="/ev/predict" element={<EVInput />} />
        <Route path="/hv/predict" element={<HVInput />} />
      </Routes>
    </Router>
  );
}

export default App;
