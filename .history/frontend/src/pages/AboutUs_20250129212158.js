import React from 'react';
import './AboutUs.css';
import AabhashImage from '../assets/Aabhash.jpg';
import KamalImage from '../assets/Kamal.jpg';
import ManishImage from '../assets/Manish.jpg';
function AboutUs() {
    return (
        <div className="about-us-container">
            <div className="about-header">
                <h1>About Us</h1>
                <p>Learn more about our team and the mission behind the medical insurance prediction system</p>
            </div>

            <div className="about-content">
                <div className="about-section">
                    <h2>Our Mission</h2>
                    <p>
                        Our mission is to provide individuals with an easy and accurate way to predict their medical insurance
                        costs, helping them make informed decisions based on key factors such as age, health metrics, and habits.
                        We aim to promote financial well-being through transparency and personalized predictions.
                    </p>
                </div>

                <div className="team-section">
                    <h2>Meet the Team</h2>
                    <div className="team-members">
                        <div className="team-member">
                            <img src={AabhashImage} alt="Team member 1" />
                            <h3>Aabhash Basnet</h3>
                            <p>Backend Developer</p>
                        </div>
                        <div className="team-member">
                            <img src={ManishImage} alt="Team member 2" />
                            <h3>Manish Karki</h3>
                            <p>Machine Learning Engineer</p>
                        </div>
                        <div className="team-member">
                            <img src={KamalImage} alt="Team member 3" />
                            <h3>Kamal Saud</h3>
                            <p>Machine Learning Enginner</p>
                        </div>
                    </div>
                </div>

                <div className="contact-section">
                    <h2>Contact Us</h2>
                    <p>If you have any questions, feel free to reach out to us:</p>
                    <ul>
                        <li>Email: support@insurancepredictor.com</li>
                        <li>Phone: (+977) 9804984249</li>
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default AboutUs;
