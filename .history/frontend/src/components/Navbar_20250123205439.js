import React, { Component } from "react";
import { NavLink } from "react-router-dom";  // Change Link to NavLink
import logo from './logo.svg';
import './NavbarStyles.css';

class Navbar extends Component {
    state = { clicked: false };

    handleClick = () => {
        this.setState({ clicked: !this.state.clicked });
    };

    render() {
        return (
            <>
                <nav>
                    <NavLink to="/">
                        <img src={logo} alt="Logo" />
                    </NavLink>

                    <div>
                        <ul id="navbar" className={this.state.clicked ? "#navbar active" : "#navbar"}>
                            <li>
                                <NavLink 
                                    to="/" 
                                    activeClassName="active" // Apply 'active' class when the route matches
                                    exact
                                >
                                    Home
                                </NavLink>
                            </li>
                            <li>
                                <NavLink 
                                    to="/get-prediction" 
                                    activeClassName="active" 
                                >
                                    Get Prediction
                                </NavLink>
                            </li>
                            <li>
                                <NavLink 
                                    to="/about-us" 
                                    activeClassName="active" 
                                >
                                    About Us
                                </NavLink>
                            </li>
                            <li>
                                <NavLink 
                                    to="/chat-with-us" 
                                    activeClassName="active" 
                                >
                                    Chat With Us
                                </NavLink>
                            </li>
                        </ul>
                    </div>

                    <div id="mobile" onClick={this.handleClick}>
                        <i id="bar" className={this.state.clicked ? 'fas fa-times' : 'fas fa-bars'}></i>
                    </div>
                </nav>
            </>
        );
    }
}

export default Navbar;
