import axios from 'axios';
import './Login.css'
import { LOGIN_API_IP, LOGIN_API_PORT } from './api';

import React, { useState, useEffect } from 'react';
function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('authToken');
        if (token) {
            setIsLoggedIn(true);
        }
    }, []);

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(`http://${LOGIN_API_IP}:${LOGIN_API_PORT}/login`, {
                email: email,
                password: password
            });
            const jwt = response.data.message
            localStorage.setItem('authToken', jwt);

            window.location.reload();
        } catch(err) {
            console.error(err);
        }
    };

    if (isLoggedIn) {
        return (
            <div>
                <h2>Bine ai venit pe moodle!</h2>
            </div>
        );
    }

    return (
        <div>
            <form onSubmit={handleLogin}>
                <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)}/><br />
                <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)}/><br />
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default Login;