import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import { useUser } from '../context/UserContext';  // Import UserContext to check login state
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import GetPrediction from "./pages/GetPrediction";
import AboutUs from "./pages/AboutUs";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import DetailsPage from "./pages/DetailsPage";
import Chatbot from "./pages/ChatBot";

function App() {
  const { user } = useUser();  // Get the current user from context

  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        {/* Protect the Get Prediction route */}
        <Route path="/get-prediction" element={user ? <GetPrediction /> : <Navigate to="/login" />} />
        <Route path="/about-us" element={<AboutUs />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/chat-bot" element={<Chatbot />} />
        <Route path="/details" element={<DetailsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
