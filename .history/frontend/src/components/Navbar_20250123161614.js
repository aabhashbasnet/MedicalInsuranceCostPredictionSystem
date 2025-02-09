import { Component } from "react";
import { NavLink } from "react-router-dom";
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
                    <Link to="/">
                        <img src={logo} alt="Logo" />
                    </Link>

                    <div>
                        <ul id="navbar" className={this.state.clicked ? "#navbar active" : "#navbar"}>
                            <li>
                                <NavLink 
                                    to="/" 
                                    className={({ isActive }) => (isActive ? "active" : "")}
                                >
                                    Home
                                </NavLink>
                            </li>
                            <li>
                                <NavLink 
                                    to="/get-prediction" 
                                    className={({ isActive }) => (isActive ? "active" : "")}
                                >
                                    Get Prediction
                                </NavLink>
                            </li>
                            <li>
                                <NavLink 
                                    to="/about-us" 
                                    className={({ isActive }) => (isActive ? "active" : "")}
                                >
                                    About Us
                                </NavLink>
                            </li>
                            <li>
                                <NavLink 
                                    to="/chat-with-us" 
                                    className={({ isActive }) => (isActive ? "active" : "")}
                                >
                                    Chat With Us
                                </NavLink>
                            </li>
                            <li>
                                <NavLink 
                                    to="/login" 
                                    className={({ isActive }) => (isActive ? "active" : "")}
                                >
                                    Login
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
