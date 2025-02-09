import { Component } from "react";
import { NavLink } from "react-router-dom";  // Ensure NavLink is imported correctly
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
                    {/* Use NavLink for the logo */}
                    <NavLink to="/" exact>
                        <img src={logo} alt="Logo" />
                    </NavLink>

                    <div>
                        <ul id="navbar" className={this.state.clicked ? "#navbar active" : "#navbar"}>
                            <li>
                                <NavLink 
                                    exact 
                                    to="/" 
                                    activeClassName="active" 
                                    className="nav-link"
                                >
                                    Home
                                </NavLink>
                            </li>
                            <li>
                                <NavLink 
                                    to="/get-prediction" 
                                    activeClassName="active" 
                                    className="nav-link"
                                >
                                    Get Prediction
                                </NavLink>
                            </li>
                            <li>
                                <NavLink 
                                    to="/about-us" 
                                    activeClassName="active" 
                                    className="nav-link"
                                >
                                    About Us
                                </NavLink>
                            </li>
                            <li>
                                <NavLink 
                                    to="/cha" 
                                    activeClassName="active" 
                                    className="nav-link"
                                >
                                    ChatBot
                                </NavLink>
                            </li>
                            <li>
                                <NavLink 
                                    to="/login" 
                                    activeClassName="active" 
                                    className="nav-link"
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
