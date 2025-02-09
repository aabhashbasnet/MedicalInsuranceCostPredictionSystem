import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import GetPrediction from "./pages/GetPrediction";
import AboutUs from "./pages/AboutUs";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import DetailsPage from "./pages/DetailsPage"; // Import the details page component

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/get-prediction" element={<GetPrediction />} />
        <Route path="/about-us" element={<AboutUs />} />
        
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        
        <Route path="/details" element={<DetailsPage />} /> {/* Route for the details page */}
      </Routes>
    </Router>
  );
}

export default App;
