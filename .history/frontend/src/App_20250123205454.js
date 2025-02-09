import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import GetPrediction from "./pages/GetPrediction";
import AboutUs from "./pages/AboutUs";
import ChatWithUs from "./pages/ChatBot";
import DetailsPage from "./pages/DetailsPage";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/get-prediction" element={<GetPrediction />} />
        <Route path="/about-us" element={<AboutUs />} />
        <Route path="/chat-with-us" element={<ChatWithUs />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/details" element={<DetailsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
