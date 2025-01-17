import React from "react";
import "./Home.css"; // Ensure this file is created and styled

function Home() {
    return (
        <div className="home-container">
            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-content">
                    <h1>Welcome to Your Medical Insurance Cost Predictor</h1>
                    <p>
                        Quickly and accurately estimate your medical insurance costs
                        based on personal parameters. Plan your future with confidence!
                    </p>
                    <a href="/get-prediction" className="btn-primary">
                        Get Started
                    </a>
                </div>
            </section>

            {/* Features Section */}
            <section className="features-section">
                <h2>Why Choose Us?</h2>
                <div className="features-container">
                    <div className="feature-card">
                        <i className="fas fa-chart-line feature-icon"></i>
                        <h3>Accurate Predictions</h3>
                        <p>Powered by machine learning for reliable results every time.</p>
                    </div>
                    <div className="feature-card">
                        <i className="fas fa-laptop feature-icon"></i>
                        <h3>User-Friendly Interface</h3>
                        <p>Designed with simplicity in mind for ease of use.</p>
                    </div>
                    <div className="feature-card">
                        <i className="fas fa-file-download feature-icon"></i>
                        <h3>Downloadable Reports</h3>
                        <p>Save your predictions as a PDF for easy sharing and reference.</p>
                    </div>
                    <div className="feature-card">
                        <i className="fas fa-comments feature-icon"></i>
                        <h3>24/7 AI Chatbot</h3>
                        <p>Get instant answers to your queries anytime, anywhere.</p>
                    </div>
                </div>
            </section>

            {/* Steps Section */}
            <section className="steps-section">
                <h2>How It Works</h2>
                <div className="steps-container">
                    <div className="step">
                        <span className="step-number">1</span>
                        <p>Fill in your details like age, BMI, and smoking habits.</p>
                    </div>
                    <div className="step">
                        <span className="step-number">2</span>
                        <p>Click the "Predict" button to generate your estimate.</p>
                    </div>
                    <div className="step">
                        <span className="step-number">3</span>
                        <p>Download your prediction report as a PDF.</p>
                    </div>
                </div>
            </section>

            {/* Call-to-Action */}
            <section className="cta-section">
                <h2>Ready to Predict Your Insurance Costs?</h2>
                <p>Get started now and take control of your financial planning!</p>
                <a href="/get-prediction" className="btn-primary">
                    Predict Now
                </a>
            </section>

            {/* Footer */}
            <footer className="home-footer">
                <p>&copy; 2024 Medical Insurance Cost Prediction. All rights reserved.</p>
            </footer>
        </div>
    );
}

export default Home;
