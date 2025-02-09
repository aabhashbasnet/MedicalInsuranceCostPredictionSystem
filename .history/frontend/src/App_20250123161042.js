import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import GetPrediction from "./pages/GetPrediction";
import AboutUs from "./pages/AboutUs";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import DetailsPage from "./pages/DetailsPage";
import Chatbot from "./pages/ChatBot"; // Import the chatbot page
import { UserProvider } from './context/UserContext'; // Import UserProvider

function App() {
  return (
    <UserProvider> {/* Wrap your component tree with UserProvider */}
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/get-prediction" element={<GetPrediction />} />
          <Route path="/about-us" element={<AboutUs />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/chat-bot" element={<Chatbot />} />
          <Route path="/details" element={<DetailsPage />} />
        </Routes>
      </Router>
    </UserProvider>
  );
}

export default App;
