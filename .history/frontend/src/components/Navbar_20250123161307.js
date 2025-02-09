import { Component } from "react";
import { Link } from "react-router-dom";
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
                            <li><Link className="active" to="/">Home</Link></li>
                            <li><Link to="/get-prediction">Get Prediction</Link></li>
                            <li><Link to="/about-us">About Us</Link></li>
                            <li><Link to="/chat-with-us">Chat With Us</Link></li>
                            <li><Link to="/Login">Login</Link></li>
                            
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
